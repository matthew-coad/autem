if __name__ == '__main__':
    import context

import autem.simulators as simulators

import unittest

class copy_id_on_start(simulators.Component):

    def __init__(self):
        simulators.Component.__init__(self, "copy_id_on_start")

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def prepare_member(self, member):
        member.configuration.test = member.id

class copy_mod_id_on_start(simulators.Component):

    def __init__(self, max):
        simulators.Component.__init__(self, "copy_mod_id_on_start")
        self.max = max

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def prepare_member(self, member):
        member.configuration.test = member.id % self.max

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
        self.assertFalse(simulation.running)
        simulation.start()
        self.assertTrue(simulation.running)
        outline = simulation.outline
        names = [ a.name for a in outline.attributes]
        self.assertTrue("test" in names)
        self.assertTrue("step" in names)
        self.assertTrue("member_id" in names)

    def test_no_duplicate_forms(self):
        simulation = simulators.Simulation("Test", [copy_mod_id_on_start(3)], population_size=10)
        simulation.start()
        self.assertEqual(len(simulation.forms), 3)

    def test_track_incarnations(self):
        simulation = simulators.Simulation("Test", [copy_mod_id_on_start(2)], population_size=4)
        simulation.start()
        self.assertEqual(simulation.members[0].incarnation, 1)
        self.assertEqual(simulation.members[1].incarnation, 1)
        self.assertEqual(simulation.members[2].incarnation, 2)
        self.assertEqual(simulation.members[3].incarnation, 2)

if __name__ == '__main__':
    unittest.main()
