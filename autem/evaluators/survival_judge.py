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

        final_round = simulation.round == simulation.rounds
        meaningful = stats.binom_test(0, n=contests, p=0.5, alternative='less') < self.p_value
        minority = victories * 2 < contests 

        if meaningful and minority and final_round:
            member.kill("Minority")
            member.evaluation.survival = "%d|%d minority" % (victories, contests)
        elif final_round:
            member.evaluation.survival = "%d|%d" % (victories, contests)
        else:
            member.evaluation.survival = None

    def record_member(self, member, record):
        if hasattr(member.evaluation, "survival"):
            record.SU_judgement = member.evaluation.survival
        else:
            record.SU_judgement = None
