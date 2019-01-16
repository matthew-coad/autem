if __name__ == '__main__':
    import context

import genetic

import pandas as pd
from io import StringIO

import unittest

class TestMemberCrossover(genetic.Component):

    def initializeMember(self, member):
        member.configuration.test = member.id

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.test = parent0.configuration.test

class HighestIdWinsBattle(genetic.Component):

    def battleMembers(self, population, member1, member2):
        return 1 if member1.id > member2.id else 2

class battles_fixture(unittest.TestCase):

    def test_final_count_ends_battle(self):

        simulation = genetic.Simulation("Test_Battle", [
            genetic.FixedPopulationSize(2),
            genetic.BattleCompetition(5,5,.5),
            HighestIdWinsBattle()])

        p1 = genetic.Population(simulation)
        p1.evaluate()
        p1.compete()
        alive = p1.alive
        self.assertEqual(len(p1.members), 2)
        self.assertEqual(len(p1.alive), 1)
        self.assertEqual(len(p1.exhausted), 0)
        self.assertEqual(len(p1.dead), 1)
        self.assertEqual(alive[0].id, 3)
        self.assertTrue(p1.members[0].parent0id == 0)
        self.assertTrue(p1.members[0].parent1id == 0)

    def test_children_restore_population(self):
        simulation = genetic.Simulation("Test_Battle", [
            TestMemberCrossover(),
            genetic.FixedPopulationSize(6),
            genetic.BattleCompetition(5,5,.5),
            HighestIdWinsBattle()])

        p1 = genetic.Population(simulation)
        p1.evaluate()
        p1.compete()
        p1.breed()
        self.assertEqual(len(p1.alive), 3)
        self.assertEqual(len(p1.children), 3)
        self.assertEqual(len(p1.alive + p1.children), 6)

    def test_next_generation_are_survivors(self):
        simulation = genetic.Simulation("Test_Battle", [
            TestMemberCrossover(),
            genetic.FixedPopulationSize(6),
            genetic.BattleCompetition(5,5,.5),
            HighestIdWinsBattle()])

        p1 = genetic.Population(simulation)
        p1.evaluate()
        p1.compete()
        p1.breed()

        p2 = genetic.Population(simulation, p1)
        self.assertEqual(len(p1.members), 6)
        self.assertTrue(p2.members[0].parent0id > 0)

if __name__ == '__main__':
    unittest.main()
