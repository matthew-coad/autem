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
        self.p_value = p_value

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        # Supply a "fitness" rating.
        # Members with a low fitness will get killed
        outline.append_attribute("fitness", Dataset.Battle, [Role.Measure], "fitness")
        outline.append_attribute("fitness_p", Dataset.Battle, [Role.Measure], "fitness_p")

    def contest_members(self, contestant1, contestant2, outcome):

        # Make sure we define these extension values
        outcome.fitness = None
        outcome.fitness_p = None

        if outcome.is_uncontested():
            return None

        if outcome.is_inconclusive():
            return None

        # Get all conclusive contests from current members where the member was contestant1.
        # We restrict it to contestant1 to stop contests being counted twice
        simulation = contestant1.simulation
        all_contests = [ c for m in simulation.members for c in m.contests if m.id == c.member1_id and c.is_conclusive() ]
        all_contests_victories = [ int(c.victor == 1) for c in all_contests]

        loser = contestant2 if outcome.victor == 1 else contestant1
        loser_contests = [ c for c in loser.contests if c.is_conclusive()]
        loser_victories = [ int(c.victor_id() == loser.id) for c in loser_contests]

        # Must have at least 3 contests each to make a comparison
        if len(all_contests) < 3 or len(loser_contests) < 3:
            return None

        # Run the t-test
        test_result = stats.ttest_ind(loser_victories, all_contests_victories)
        outcome.fitness = test_result[0] # positive if 1 > 2
        outcome.fitness_p = test_result[1]
        required_p_value = self.p_value

        # Need at least the required p-value to have an outcome
        if outcome.fitness_p > required_p_value:
            return None

        if outcome.fitness < 0:
            outcome.fatal()

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contests[-1] if member.contests else None
        record.fitness = outcome.fitness if outcome and outcome.loser_id() == member.id else None
        record.fitness_p = outcome.fitness_p if outcome and outcome.loser_id() == member.id else None
