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

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        # Supply a "fitness" rating.
        # Members with a low fitness will get killed
        outline.append_attribute("robustness", Dataset.Battle, [Role.Measure], "robustness")
        outline.append_attribute("attractivness", Dataset.Battle, [Role.Measure], "attractivness")

    def fate_members(self, contestant1, contestant2, outcome):

        # Make sure we define these extension values
        outcome.robustness = None
        outcome.attractivness = None

        # determine how long a record we will examine
        record_length = min(len(contestant1.wonlost), len(contestant2.wonlost))

        loser = contestant2 if outcome.victor == 1 else contestant1
        winner = contestant1 if outcome.victor == 1 else contestant2

        loser_victories = sum(loser.wonlost[-record_length:])
        winner_victories = sum(winner.wonlost[-record_length:])

        robustness_p = stats.binom_test(loser_victories, n=record_length, p=0.5, alternative='less')
        attractivness_p = stats.binom_test(winner_victories, n=record_length, p=0.5, alternative='greater')

        if robustness_p < self.p_value:
            outcome.fatal()

        if attractivness_p < self.p_value:
            outcome.hubba()

        outcome.robustness = robustness_p
        outcome.attractivness = 1 - attractivness_p

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contest
        record.robustness = outcome.robustness if outcome and outcome.loser_id() == member.id else None
        record.attractivness = outcome.attractivness if outcome and outcome.victor_id() == member.id else None
