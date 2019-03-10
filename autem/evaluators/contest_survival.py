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

        # If the winner is in the same or lower league than the loser
        # determine if the winner should be promoted
        if winner.league <= loser.league:
            power_p = stats.binom_test(winner_victories, n=record_length, p=0.5, alternative='greater')
            promote = power_p < self.p_value

            if promote:
                winner.promote()
                winner.evaluation.contest_survival = "%d|%d promotion" % (winner_victories, loser_victories)
            else:
                winner.evaluation.contest_survival = "%d|%d win" % (winner_victories, loser_victories)
        else:
            winner.evaluation.contest_survival = "mismatch win"

        # Determine if the loser should be eliminated
        robustness_p = stats.binom_test(loser_victories, n=record_length, p=0.5, alternative='less')
        eliminate = robustness_p < self.p_value
        if eliminate:
            loser.eliminate()
            loser.evaluation.contest_survival = "%d|%d elimination" % (loser_victories, winner_victories)
        else:
            loser.evaluation.contest_survival = "%d|%d loss" % (loser_victories, winner_victories)

    def record_member(self, member, record):
        if hasattr(member.evaluation, "contest_survival"):
            record.contest_survival = member.evaluation.contest_survival
        else:
            record.contest_survival = None
