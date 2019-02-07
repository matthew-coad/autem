from ..simulators import Dataset, Role
from .contester import Contester

import numpy as np
from scipy import stats
 
class Survival(Contester):
    """
    After a contest check who lives and who dies.
    Compares the losers defeats against that of the general population. If its significanly more then its adios muchachos.
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the survival history is significanly different from the general populations
        """
        Contester.__init__(self, "BestLearner")
        self.p_value = p_value

    def stress_members(self, contestant1, contestant2, outcome):

        # determine how long a record we will examine
        record_length = min(len(contestant1.wonlost), len(contestant2.wonlost))

        loser = contestant2 if outcome.victor == 1 else contestant1
        winner = contestant1 if outcome.victor == 1 else contestant2

        loser_victories = sum(loser.wonlost[-record_length:])
        winner_victories = sum(winner.wonlost[-record_length:])

        attractivness_p = stats.binom_test(winner_victories, n=record_length, p=0.5, alternative='greater')
        attractive = 1 if attractivness_p < self.p_value else 0
        winner.checked_out(1 - attractivness_p, attractive)

        robustness_p = stats.binom_test(loser_victories, n=record_length, p=0.5, alternative='less')
        fatality = 1 if robustness_p < self.p_value else 0
        loser.stressed(robustness_p, fatality)

