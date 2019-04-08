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

    def judge_member(self, member):
        member.evaluation.promotion  = None

        simulation = member.simulation
        all_contests = [ m.contests for m in simulation.members ]
        max_contests = min(member.contests, int(np.mean(all_contests)))
        if max_contests == 0:
            return None

        wonlost = member.wonlost[-max_contests:]
        victories = sum(wonlost)

        top_league = simulation.top_league
        power_p = stats.binom_test(victories, n=max_contests, p=0.5, alternative='greater')
        powerful = power_p < self.p_value
        maxed = member.league == top_league
        promote = powerful and not maxed

        if promote:
            member.evaluation.promotion = "%d|%d promote" % (victories, max_contests)
            member.promote()
        elif promote and maxed:
            member.evaluation.promotion = "%d|%d maxed" % (victories, max_contests)
        else:
            member.evaluation.promotion = "%d|%d" % (victories, max_contests)

    def record_member(self, member, record):
        if hasattr(member.evaluation, "promotion"):
            record.promotion = member.evaluation.promotion
        else:
            record.promotion = None
