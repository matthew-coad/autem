if __name__ == '__main__':
    import context

import genetic

import pandas as pd

import unittest

class TestFlagMemberEvaluated(genetic.Component):

    def initializeMember(self, member):
        member.configuration.evaluated = False

    def evaluateMember(self, member):
        member.configuration.evaluated = True

class TestSaveId(genetic.Component):

    def evaluateMember(self, member):
        member.evaluation.test = member.id

    def reportMember(self, member, row):
        row.test = member.evaluation.test

class populations_fixture(unittest.TestCase):

    def test_populations_have_unique_id(self):
        simulation = genetic.Simulation("Test", [])
        population1 = genetic.Population(simulation)
        population2 = genetic.Population(simulation)
        self.assertNotEqual(population1.id, population2.id)

    def test_has_fixed_size_members(self):
        simulation = genetic.Simulation("Test", [genetic.FixedPopulationSize(10)])
        population1 = genetic.Population(simulation)
        self.assertEqual(len(population1.members), 10)

    def test_members_evaluated(self):
        simulation = genetic.Simulation("Test", [
            genetic.FixedPopulationSize(10),
            TestFlagMemberEvaluated()
            ])
        population1 = genetic.Population(simulation)
        population1.evaluate()
        self.assertEqual(len(population1.members), 10)
        self.assertTrue(population1.members[0].configuration.evaluated)

    def test_population_report(self):
        simulation = genetic.Simulation("Test", [
            genetic.FixedPopulationSize(10),
            TestSaveId()
            ])
        population1 = genetic.Population(simulation)
        population1.evaluate()
        population1.analyze()

        report = population1.population_report
        check_report = report[['generation_prop', 'population_id']]
        expected_report = pd.DataFrame(data  = {'generation_prop': [1], 'population_id': [1]})
        self.assertTrue(check_report.equals(expected_report))

if __name__ == '__main__':
    unittest.main()
