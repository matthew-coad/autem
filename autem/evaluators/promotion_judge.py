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

    def start_epoch(self, epoch):
        """
        Start a simulation epoch
        """
        simulation = epoch.simulation
        members = simulation.list_members()
        for member in members:
            member.evaluation.promotion = None

    def judge_member(self, member):
        simulation = member.simulation
        epoch_id = simulation.epoch.id

        wonlost = member.wonlost[epoch_id]
        contests = len(wonlost)
        victories = sum(wonlost)

        top_league = simulation.top_league
        #power_p = stats.binom_test(victories, n=contests, p=0.5, alternative='greater')
        #powerful = power_p < self.p_value
        maxed = member.league == top_league
        final_round = simulation.round == simulation.round_size
        majority = victories * 2 > contests and stats.binom_test(0, n=contests, p=0.5, alternative='less') < self.p_value

        if final_round and majority and not maxed:
            member.evaluation.promotion = "%d|%d majority" % (victories, contests)
            member.promote("Majority")
        elif final_round and majority and maxed:
            member.evaluation.promotion = "%d|%d maxed" % (victories, contests)
        elif final_round:
            member.evaluation.promotion = "%d|%d" % (victories, contests)
        else:
            member.evaluation.promotion = None

    def record_member(self, member, record):
        contest_judgement = get_contest
        if hasattr(member.evaluation, "promotion"):
            record.PR_judgement = member.evaluation.promotion
        else:
            record.PR_judgement = None
