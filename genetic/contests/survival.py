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
        outline.append_attribute("survive_p", Dataset.Battle, [Role.Measure], "survive_p")
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
        loser_victories = loser.n_victory
        loser_defeats = loser.n_defeat
        loser_contests = loser_victories + loser_defeats

        winner = contestant1 if outcome.victor == 1 else contestant2
        winner_victories = winner.n_victory
        winner_defeats = winner.n_defeat
        winner_contests = winner_victories + winner_defeats

        total_victories = sum(m.n_victory for m in simulation.members)
        total_defeats = sum(m.n_defeat for m in simulation.members)
        total_contests = total_victories + total_defeats
        if total_contests < 10:
            return None

        total_p = total_victories / total_contests

        survive_p = stats.binom_test(loser_victories, n=loser_contests, p=total_p, alternative='less')
        attractive_p = stats.binom_test(winner_victories, n=winner_contests, p=total_p, alternative='greater')

        if survive_p < self.p_value:
            outcome.fatal()

        if attractive_p < self.p_value:
            outcome.hubba()

        outcome.survive_p = survive_p
        outcome.attractive_p = attractive_p

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contests[-1] if member.contests else None
        record.survive_p = outcome.survive_p if outcome and outcome.loser_id() == member.id else None
        record.attractive_p = outcome.attractive_p if outcome and outcome.victor_id() == member.id else None
