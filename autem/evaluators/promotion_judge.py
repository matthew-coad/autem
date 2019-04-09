from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats
 
class PromotionJudge(Evaluater):
    """
    Judge that determines if a member get promoted
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        self.p_value = p_value

    def start_epoch(self, simulation):
        """
        Start a simulation epoch
        """
        members = simulation.list_members()
        for member in members:
            member.evaluation.promotion = None

    def judge_member(self, member):
        simulation = member.simulation
        epoch = simulation.epoch

        wonlost = member.wonlost[epoch]
        contests = len(wonlost)
        victories = sum(wonlost)

        top_league = simulation.top_league
        power_p = stats.binom_test(victories, n=contests, p=0.5, alternative='greater')
        powerful = power_p < self.p_value
        maxed = member.league == top_league
        promote = powerful and not maxed

        if promote:
            member.evaluation.promotion = "%d|%d promote" % (victories, contests)
            member.promote("Powerful")
        elif promote and maxed:
            member.evaluation.promotion = "%d|%d maxed" % (victories, contests)
        else:
            member.evaluation.promotion = "%d|%d" % (victories, contests)

    def record_member(self, member, record):
        if hasattr(member.evaluation, "promotion"):
            record.promotion = member.evaluation.promotion
        else:
            record.promotion = None
