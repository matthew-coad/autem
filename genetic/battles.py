from .components import Component
from . import members
from . import populations

from math import floor


class BattleCompetition(Component):

    """
    A Battle competition has population members engage in a series of "contests" to determine which members are fittest.
    Each member starts with a number of hit points which the loose after each loss. The member is eliminated if they run out
    of hitpoints. 
    
    The contest may also be considered a draw in which case both contestants lose "energy". Members that run out of energy are eliminated
    from further contests but stay alive.

    The idea is to find the fittest members without having to generate a specific "score" per member as many
    interesting statistical tests only allow comparison between populations and don't provide an objective "score".
    """

    def __init__(self, hit_points, energy_points, survivor_ratio):
        self.hit_points = hit_points
        self.energy_points = energy_points
        self.survivor_ratio = survivor_ratio

    def runBattle(self, population, member1, member2):
        """
        Run a battle between two members.
        Returns the member postfix of the victor, 0 if the contest is a draw
        """
        # Run battles in order until we get a result
        for component in population.simulation.components:
            result = component.battleMembers(population, member1, member2)
            if result > 0:
                return result
        return 0

    def competePopulation(self, population):
        """
        Have members of the population compete in a series of battles.
        Each contestant starts with a number of "hitpoints" and "energy". 
        Every they lose a battle they lose a hitpoint and are eliminated from
        the population if they run out of hitpoints.
        If the battle is a draw both contestants lose a point of energy. If a battle has
        a result both contestants gain a point of energy.
        If a contestant out of energy they become exhausted and can no longer compete 
        in competitions.

        The competition runs until a preset number of members are dead or all competitors
        are exhausted.

        The idea is have members to continue battling until we have a population of "fit"
        members or can't determine fitness anymore.
        """
        alive = population.alive
        exhausted = population.exhausted
        dead = population.dead
        initial_hit_points = self.hit_points
        initial_energy_points = self.energy_points
        survivor_ratio = self.survivor_ratio
        minimum_members =  floor(len(alive) * survivor_ratio)
        random_state = population.simulation.random_state

        for member in alive:
            member.evaluation.battles = 0
            member.evaluation.hit_points = initial_hit_points
            member.evaluation.energy = initial_energy_points

        while (len(alive)+ len(exhausted) > minimum_members and len(alive) > 1):
            contestant_indexes = random_state.choice(len(alive), 2, replace=False)
            
            contest_result = self.runBattle(population, alive[contestant_indexes[0]], alive[contestant_indexes[1]])
            alive[contestant_indexes[0]].evaluation.battles += 1
            alive[contestant_indexes[1]].evaluation.battles += 1

            member.evaluation.battles = 0
            if contest_result == 1:
                alive[contestant_indexes[1]].evaluation.hit_points -= 1
                alive[contestant_indexes[0]].evaluation.energy += 1
                alive[contestant_indexes[1]].evaluation.energy += 1
                if alive[contestant_indexes[1]].evaluation.hit_points <= 0:
                    dead.append(alive[contestant_indexes[1]])
                    del alive[contestant_indexes[1]]
            elif contest_result == 2:
                alive[contestant_indexes[0]].evaluation.hit_points -= 1
                alive[contestant_indexes[0]].evaluation.energy += 1
                alive[contestant_indexes[1]].evaluation.energy += 1
                if alive[contestant_indexes[0]].evaluation.hit_points <= 0:
                    dead.append(alive[contestant_indexes[0]])
                    del alive[contestant_indexes[0]]
            else:
                alive[contestant_indexes[0]].evaluation.energy -= 1
                alive[contestant_indexes[1]].evaluation.energy -= 1
                # Remove contestant with highest id first to stop 1st index changing
                sorted_indexes = sorted(contestant_indexes)
                if alive[sorted_indexes[1]].evaluation.energy <= 0:
                    exhausted.append(alive[sorted_indexes[0]])
                    del alive[sorted_indexes[1]]
                if alive[sorted_indexes[0]].evaluation.energy <= 0:
                    exhausted.append(alive[sorted_indexes[0]])
                    del alive[sorted_indexes[0]]

        # Competition over
        population.alive = alive
        population.exhausted = exhausted
        population.dead = dead

    def reportMember(self, member, row):
        row.n_battle_measure = member.evaluation.battles
        row.hp_measure = member.evaluation.hit_points
        row.energy_measure = member.evaluation.energy

