from ..member_manager import MemberManager
from ..epoch_manager import EpochManager
from ..reporters import Reporter

import numpy as np
from scipy import stats

class ContestJudgement:

    def __init__(self):
        self.contests = None
        self.victories = None
        self.meaningful = None
        self.outcome = None
        

def get_contest_judgement(member):
    """
    Get contest judgement for a member
    """
    judgment = member.get_state("contest_judgement", lambda: ContestJudgement())
    return judgment

def reset_contest_judgement(member):
    """
    Reset contest judgement for a member
    """
    member.set_state("contest_judgement", ContestJudgement())

class ContestJudge(MemberManager, EpochManager, Reporter):
    """
    Contest judgements
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        self.p_value = p_value

    def prepare_epoch(self, epoch):
        members = epoch.list_members()
        for member in members:
            reset_contest_judgement(member)

    def judge_member(self, member):

        reset_contest_judgement(member)
        judgement = get_contest_judgement(member)

        specie = member.get_specie()
        epoch = specie.get_current_epoch()

        if not member.alive:
            judgement.outcome = member.event
            return None

        wonlost = member.wonlost
        contests = len(wonlost)
        victories = sum(wonlost)

        meaningful = stats.binom_test(0, n=contests, p=0.5, alternative='less') < self.p_value
        majority = victories * 2 > contests

        if meaningful and majority:
            outcome = "Fit"
        elif meaningful and not majority:
            outcome = "Unfit"
            member.kill(outcome)
        elif not meaningful:
            outcome = "Few contests"
        else:
            raise RuntimeError("Unexpected condition")

        judgement.contests = contests
        judgement.victories = victories
        judgement.meaningful = meaningful
        judgement.outcome = outcome

    def record_member(self, member, record):
        judgement = get_contest_judgement(member)

        record.CJ_contests = judgement.contests
        record.CJ_victories = judgement.victories
        record.CJ_outcome = judgement.outcome
