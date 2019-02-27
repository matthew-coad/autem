from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats
 
class ContestSurvival(Evaluater):
    """
    After a contest check who lives and who dies.
    Compares the losers defeats against that of the general population. If its significanly more then its adios muchachos.
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        self.p_value = p_value

    def stress_members(self, contestant1, contestant2, outcome):

        contestant1.evaluation.contest_survival = None
        contestant2.evaluation.contest_survival = None

        # determine how long a record we will examine
        record_length = min(len(contestant1.wonlost), len(contestant2.wonlost))
        if record_length == 0:
            return None

        loser = contestant2 if outcome.victor == 1 else contestant1
        winner = contestant1 if outcome.victor == 1 else contestant2

        loser_victories = sum(loser.wonlost[-record_length:])
        winner_victories = sum(winner.wonlost[-record_length:])

        attractivness_p = stats.binom_test(winner_victories, n=record_length, p=0.5, alternative='greater')
        famous = 1 if attractivness_p < self.p_value else 0
        winner.nominated(1 - attractivness_p, famous)
        if famous:
            winner.evaluation.contest_survival = "%d|%d nomination" % (winner_victories, loser_victories)
        else:
            winner.evaluation.contest_survival = "%d|%d" % (winner_victories, loser_victories)

        robustness_p = stats.binom_test(loser_victories, n=record_length, p=0.5, alternative='less')
        fatality = 1 if robustness_p < self.p_value else 0
        loser.stressed(robustness_p, fatality)

        if fatality:
            loser.evaluation.contest_survival = "%d|%d fatal" % (loser_victories, winner_victories)
        else:
            loser.evaluation.contest_survival = "%d|%d" % (loser_victories, winner_victories)


    def record_member(self, member, record):
        if hasattr(member.evaluation, "contest_survival"):
            record.contest_survival = member.evaluation.contest_survival
        else:
            record.contest_survival = None
