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
        outline.append_attribute("fatality_p", Dataset.Battle, [Role.Measure], "fatality_p")
        outline.append_attribute("attractive_p", Dataset.Battle, [Role.Measure], "attractive_p")

    def contest_members(self, contestant1, contestant2, outcome):

        # Make sure we define these extension values
        outcome.survive_p = None
        outcome.attractive_p = None

        if outcome.is_uncontested():
            return None

        if outcome.is_inconclusive():
            return None

        # Get all conclusive contests from current members where the member was contestant1.
        # We restrict it to contestant1 to stop contests being counted twice
        simulation = contestant1.simulation
        loser = contestant2 if outcome.victor == 1 else contestant1
        loser_victories = loser.victories
        loser_defeats = loser.defeats
        loser_contests = loser_victories + loser_defeats

        winner = contestant1 if outcome.victor == 1 else contestant2
        winner_victories = winner.victories
        winner_defeats = winner.defeats
        winner_contests = winner_victories + winner_defeats

        fatality_p = stats.binom_test(loser_victories, n=loser_contests, p=0.5, alternative='less')
        attractive_p = stats.binom_test(winner_victories, n=winner_contests, p=0.5, alternative='greater')

        if fatality_p < self.p_value:
            outcome.fatal()

        if attractive_p < self.p_value:
            outcome.hubba()

        outcome.fatality_p = 1 - fatality_p
        outcome.attractive_p = 1 - attractive_p

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contest
        record.survive_p = outcome.survive_p if outcome and outcome.loser_id() == member.id else None
        record.attractive_p = outcome.attractive_p if outcome and outcome.victor_id() == member.id else None
