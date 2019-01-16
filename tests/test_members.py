if __name__ == '__main__':
    import context

import genetic

from types import SimpleNamespace
import numpy as np
import pandas as pd

import unittest

class TestMemberInitializer(genetic.Component):

    def initializeMember(self, member):
        member.configuration.test = 1

class TestMemberCrossover(genetic.Component):

    def initializeMember(self, member):
        member.configuration.test = member.id

    def copyMember(self, member, parent0):
        member.configuration.test = parent0.configuration.test

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.test = parent1.configuration.test

class TestReportId(genetic.Component):

    def evaluateMember(self, member):
        member.evaluation.test = member.id

    def reportMember(self, member, row):
        row.test = member.evaluation.test

class members_fixture(unittest.TestCase):

    def test_members_have_unique_ids(self):
        simulation = genetic.Simulation("Test", [])
        population1 = genetic.Population(simulation)
        member1 = genetic.Member(population1)
        member2 = genetic.Member(population1)
        self.assertNotEqual(member1.id, member2.id)

    def test_new_members_are_initialized(self):
        testSimulation = genetic.Simulation("Test", [TestMemberInitializer()])
        testPopulation = genetic.Population(testSimulation)
        testMember = genetic.Member(testPopulation)
        self.assertTrue(isinstance(testMember, genetic.Member))
        self.assertEqual(testMember.configuration.test, 1)

    def test_copy(self):
        testSimulation = genetic.Simulation("Test", [TestMemberCrossover()])
        testPopulation = genetic.Population(testSimulation)
        parent0 = genetic.Member(testPopulation)
        testMember = genetic.Member(testPopulation, parent0)
        self.assertEqual(testMember.configuration.test, parent0.configuration.test)

    def test_crossover(self):
        testSimulation = genetic.Simulation("Test", [TestMemberCrossover()])
        testPopulation = genetic.Population(testSimulation)
        parent0 = genetic.Member(testPopulation)
        parent1 = genetic.Member(testPopulation)
        testMember = genetic.Member(testPopulation, parent0, parent1)
        self.assertEqual(testMember.configuration.test, parent1.configuration.test)

    def test_member_report_row(self):
        simulation = genetic.Simulation("Test", [
            genetic.FixedPopulationSize(10),
            TestReportId()
            ])
        population1 = genetic.Population(simulation)
        population1.evaluate()
        member0 = population1.members[0]
        row = member0.report()
        self.assertTrue(row.test == member0.id)

    def test_member_report(self):
        simulation = genetic.Simulation("Test", [
            genetic.FixedPopulationSize(5),
            TestReportId()
            ])
        population1 = genetic.Population(simulation)
        population1.evaluate()
        population1.analyze()
        frame = population1.member_report
        check_report = frame[['generation_prop', 'population_id', 'member_id', 'test']]
        test_frame = pd.DataFrame(data  = {'generation_prop': [1,1,1,1,1], 'population_id': [1,1,1,1,1], 'member_id': [2,3,4,5,6], 'test': [2,3,4,5,6]})
        self.assertTrue(check_report.equals(test_frame))

if __name__ == '__main__':
    unittest.main()
