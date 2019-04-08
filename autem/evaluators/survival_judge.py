from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats
 
class SurvivalJudge(Evaluater):
    """
    Judge that determines if a member survives
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        self.p_value = p_value

    def judge_member(self, member):

        member.evaluation.survival = None
        simulation = member.simulation
        all_contests = [ m.contests for m in simulation.members ]
        max_contests = min(member.contests, int(np.mean(all_contests)))
        if max_contests == 0:
            return None

        wonlost = member.wonlost[-max_contests:]
        victories = sum(wonlost)

        robustness_p = stats.binom_test(victories, n=max_contests, p=0.5, alternative='less')
        kill = robustness_p < self.p_value
        if kill:
            member.kill("Unfit")
            member.evaluation.survival = "%d|%d die" % (victories, max_contests)
        else:
            member.evaluation.survival = "%d|%d" % (victories, max_contests)

    def judge_members(self, contestant1, contestant2):
        self.judge_member(contestant1)
        self.judge_member(contestant2)

    def record_member(self, member, record):
        if hasattr(member.evaluation, "survival"):
            record.survival = member.evaluation.survival
        else:
            record.survival = None
