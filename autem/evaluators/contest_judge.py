from .. import Dataset, Role
from .evaluator import Evaluater

from .contest_judgement import ContestJudgement,get_contest_judgement

import numpy as np
from scipy import stats
 
class ContestJudge(Evaluater):
    """
    Contest judgements
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        self.p_value = p_value

    def start_epoch(self, simulation):
        members = simulation.list_members()
        for member in members:
            member.evaluation.survival = None

    def judge_member(self, member):

        judgement = ContestJudgement()
        member.evaluation.contest_judgement = judgement

        simulation = member.simulation
        epoch = simulation.epoch

        if not member.alive:
            judgement.outcome = member.event_reason
            return None

        wonlost = member.wonlost[epoch]
        contests = len(wonlost)
        victories = sum(wonlost)

        meaningful = stats.binom_test(0, n=contests, p=0.5, alternative='less') < self.p_value
        majority = victories * 2 > contests
        top_league = simulation.top_league

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
