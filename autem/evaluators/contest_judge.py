from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats
 
class ContestJudge(Evaluater):
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
        simulation = contestant1.simulation

        max_contests = min(len(contestant1.wonlost), len(contestant2.wonlost))
        if max_contests == 0:
            return None

        loser = contestant2 if outcome.victor == 1 else contestant1
        loser_wonlost = loser.wonlost[-max_contests:]
        loser_victories = sum(loser_wonlost)
        winner = contestant1 if outcome.victor == 1 else contestant2
        winner_wonlost = winner.wonlost[-max_contests:]
        winner_victories = sum(winner_wonlost)

        # Determine if the loser should be eliminated
        robustness_p = stats.binom_test(loser_victories, n=max_contests, p=0.5, alternative='less')
        eliminate = robustness_p < self.p_value
        if eliminate:
            loser.eliminate()
            winner.eliminator()
            loser.evaluation.contest_survival = "%d|%d eliminate" % (loser_victories, max_contests)
        else:
            loser.evaluation.contest_survival = "%d|%d survive" % (loser_victories, max_contests)

        top_league = simulation.top_league
        if winner.league < loser.league:
            # If the winner is in a lower league then its an upset.
            winner.evaluation.contest_survival = "%d|%d upset " % (loser.league, winner.league)
            winner.promote()
        elif winner.league == loser.league:
            # If the winner is in the same league and its persistently winning members then promote it
            power_p = stats.binom_test(winner_victories, n=max_contests, p=0.5, alternative='greater')
            powerful = power_p < self.p_value
            maxed = winner.league == top_league
            promote = powerful and not maxed

            if promote:
                winner.evaluation.contest_survival = "%d promote" % (winner.eliminations)
                winner.promote()
            elif maxed:
                winner.evaluation.contest_survival = "%d maxed" % (winner.eliminations)
            else:
                winner.evaluation.contest_survival = "%d stay" % (winner.eliminations)
        else:
            winner.evaluation.contest_survival = "win mismatch"

    def record_member(self, member, record):
        if hasattr(member.evaluation, "contest_survival"):
            record.contest_survival = member.evaluation.contest_survival
        else:
            record.contest_survival = None
