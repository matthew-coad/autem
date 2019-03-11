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

    def judge_members(self, contestant1, contestant2, outcome):
        contestant1.evaluation.contest_survival = None
        contestant2.evaluation.contest_survival = None

        loser = contestant2 if outcome.victor == 1 else contestant1
        winner = contestant1 if outcome.victor == 1 else contestant2

        # Determine if the loser should be eliminated
        robustness_p = stats.binom_test(loser.victories, n=loser.contests, p=0.5, alternative='less')
        eliminate = robustness_p < self.p_value
        if eliminate:
            loser.eliminate()
            winner.eliminator()
            loser.evaluation.contest_survival = "%d|%d eliminate" % (loser.victories, loser.contests)
        else:
            loser.evaluation.contest_survival = "%d|%d survive" % (loser.victories, loser.contests)

        if winner.league < loser.league:
            # If the winner is in a lower league then its an upset. Immediately promote them to the losers league
            winner.promote(loser.league)
            winner.evaluation.contest_survival = "%d|%d upset " % (loser.league, winner.league)
        elif winner.league == loser.league:
            # If the winner is in the same league and its persistently eliminating members then promote it
            power_p = stats.binom_test(winner.eliminations, n=winner.eliminations, p=0.5, alternative='greater')
            promote = power_p < self.p_value

            if promote:
                winner.promote()
                winner.evaluation.contest_survival = "%d promote" % (winner.eliminations)
            else:
                winner.evaluation.contest_survival = "%d remain" % (winner.eliminations)
        else:
            winner.evaluation.contest_survival = "mismatch"

    def record_member(self, member, record):
        if hasattr(member.evaluation, "contest_survival"):
            record.contest_survival = member.evaluation.contest_survival
        else:
            record.contest_survival = None
