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

    def start_epoch(self, simulation):
        members = simulation.list_members()
        for member in members:
            member.evaluation.survival = None

    def judge_member(self, member):

        member.evaluation.survival = None
        simulation = member.simulation
        epoch = simulation.epoch

        wonlost = member.wonlost[epoch]
        contests = len(wonlost)
        victories = sum(wonlost)

        robustness_p = stats.binom_test(victories, n=contests, p=0.5, alternative='less')
        kill = robustness_p < self.p_value
        if kill:
            member.kill("Unfit")
            member.evaluation.survival = "%d|%d die" % (victories, contests)
        else:
            member.evaluation.survival = "%d|%d" % (victories, contests)

    def record_member(self, member, record):
        if hasattr(member.evaluation, "survival"):
            record.survival = member.evaluation.survival
        else:
            record.survival = None
