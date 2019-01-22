if __name__ == '__main__':
    import context

import genetic.simulators as simulators

import unittest

class copy_id_on_start(simulators.Component):

    def outline_simulation(self, simulation, outline):
        outline.make_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def start_member(self, member):
        member.configuration.test = member.id

class simulation_startup_fixture(unittest.TestCase):

    def test_population_size_after_start(self):
        simulation = simulators.Simulation("Test", [], population_size=10)
        simulation.start()
        self.assertEqual(len(simulation.members), 10)

    def test_members_have_unique_id(self):
        simulation = simulators.Simulation("Test", [], population_size=3)
        simulation.start()
        self.assertNotEqual(simulation.members[0].id,simulation.members[1].id)
        self.assertNotEqual(simulation.members[0].id,simulation.members[2].id)
        self.assertNotEqual(simulation.members[1].id,simulation.members[2].id)

    def test_member_start(self):
        simulation = simulators.Simulation("Test", [copy_id_on_start()], population_size=10)
        simulation.start()
        member = simulation.members[0]
        self.assertEqual(member.configuration.test, member.id)

    def test_standard_outline(self):
        simulation = simulators.Simulation("Test", [], population_size=10)
        simulation.start()
        outline = simulation.outline
        names = [ a.name for a in outline.attributes]
        self.assertTrue("step" in names)
        self.assertTrue("member_id" in names)


    def test_custom_outline(self):
        simulation = simulators.Simulation("Test", [copy_id_on_start()], population_size=10)
        simulation.start()
        outline = simulation.outline
        names = [ a.name for a in outline.attributes]
        self.assertTrue("test" in names)
        self.assertTrue("step" in names)
        self.assertTrue("member_id" in names)

if __name__ == '__main__':
    unittest.main()
