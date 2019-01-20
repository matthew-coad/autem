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
        Run a match between two members.
        Returns the member postfix of the victor, 0 if the contest is a draw
        """
        # Run battles in order until we get a result
        for component in population.simulation.components:
            result = component.battleMembers(population, member1, member2)
            if result > 0:
                return result
        return 0

    def battlePopulation(self, population):
        """
        Have members of the population battle in a series of matches.
        Each contestant starts with a number of "hitpoints" and "energy". 
        Every they lose a battle they lose a hitpoint and are eliminated from
        the population if they run out of hitpoints.
        If the battle is a draw both contestants lose a point of energy. If a battle has
        a result both contestants gain a point of energy.
        If a contestant out of energy they become exhausted and can no longer compete 
        in matches.

        The competition runs until a preset number of members are dead or all competitors
        are exhausted.

        The idea is have members to continue battling until we have a population of "fit"
        members or can't determine fitness anymore.
        """
        alive = population.alive
        exhausted = population.exhausted
        dead = population.dead
        passive = population.passive
        finalising = population.finalising

        initial_hit_points = self.hit_points
        initial_energy_points = self.energy_points
        survivor_ratio = self.survivor_ratio
        if not finalising:
            minimum_members =  floor(len(alive) * survivor_ratio)
        else:
            minimum_members = 0

        random_state = population.simulation.random_state

        for member in alive:
            member.evaluation.battles = 0
            member.evaluation.hit_points = initial_hit_points
            member.evaluation.energy = initial_energy_points
            member.evaluation.passive = False

        while (len(alive) + len(exhausted) > minimum_members and len(alive) > 1):
            contestant_indexes = random_state.choice(len(alive), 2, replace=False)

            if not repr(alive[contestant_indexes[0]].configuration) == repr(alive[contestant_indexes[1]].configuration):
                contest_result = self.runBattle(population, alive[contestant_indexes[0]], alive[contestant_indexes[1]])
            else:
                # Members are identical! Set the contest result to No contest
                contest_result = -1

            # Energy, battles evaluation
            if contest_result == 1 or contest_result == 2:
                # Someone won!
                # Mark the battles and give both contestant a point of energy to keep them fighting.
                # Cos something interesting is happening
                alive[contestant_indexes[0]].evaluation.battles += 1
                alive[contestant_indexes[1]].evaluation.battles += 1
                alive[contestant_indexes[0]].evaluation.energy += 1
                alive[contestant_indexes[1]].evaluation.energy += 1
            elif contest_result == 0:
                # Draw
                # Mark the battles but remove a point of energy to exhaust the contestants
                # if no outcome can be decided
                alive[contestant_indexes[0]].evaluation.battles += 1
                alive[contestant_indexes[1]].evaluation.battles += 1
                alive[contestant_indexes[0]].evaluation.energy -= 1
                alive[contestant_indexes[1]].evaluation.energy -= 1
            else:
                # No contest
                pass

            # Hp/passive evauation
            if contest_result == 1:
                alive[contestant_indexes[1]].evaluation.hit_points -= 1
            elif contest_result == 2:
                alive[contestant_indexes[0]].evaluation.hit_points -= 1
            elif contest_result == 0:
                pass
            else:
                alive[contestant_indexes[0]].evaluation.passive = True

            # Process contestant in index order to stop the index changing if we delete 
            sorted_indexes = sorted(contestant_indexes)

            def process_contestant(index):
                contestant = alive[index]
                if contestant.evaluation.hit_points <= 0:
                    dead.append(contestant)
                    del alive[index]
                elif contestant.evaluation.energy <= 0:
                    exhausted.append(contestant)
                    del alive[index]
                elif contestant.evaluation.passive:
                    passive.append(contestant)
                    del alive[index]
                else:
                    pass
            process_contestant(sorted_indexes[1])
            process_contestant(sorted_indexes[0])

        # Competition over
        population.alive = alive
        population.exhausted = exhausted
        population.dead = dead
        population.passive = passive

        if finalising:
            population.complete = len(alive) + len(exhausted) <= 1

    def reportMember(self, member, row):
        row.n_battle_measure = member.evaluation.battles
        row.hp_measure = member.evaluation.hit_points
        row.energy_measure = member.evaluation.energy
        row.passive_measure = member.evaluation.passive

