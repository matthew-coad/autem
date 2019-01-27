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
        loser = contestant2 if outcome.victor == 1 else contestant1
        loser_contests = [ c for c in loser.contests if c.is_conclusive()]
        n_loser_contests = len(loser_contests)

        if n_loser_contests < 3:
            return None

        n_loser_victories = sum([ int(c.victor_id() == loser.id) for c in loser_contests])

        all_contests = [ c for m in simulation.members for c in m.contests if m.id == c.member1_id and c.is_conclusive() and c.member1_id != loser.id and c.member2_id != loser.id ]
        n_all_contests = len(all_contests)
        if n_all_contests < 3:
            return None

        n_all_contests_victories = sum([ int(c.victor == 1) for c in all_contests])
        all_p = n_all_contests_victories / n_all_contests

        test_result = stats.binom_test(n_loser_victories, n=n_loser_contests, p=all_p, alternative='less')
        outcome.fitness_p = test_result
        required_p_value = self.p_value

        # Need at least the required p-value to have an outcome
        if outcome.fitness_p > required_p_value:
            return None
        outcome.fatal()

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contests[-1] if member.contests else None
        record.fitness = outcome.fitness if outcome and outcome.loser_id() == member.id else None
        record.fitness_p = outcome.fitness_p if outcome and outcome.loser_id() == member.id else None
