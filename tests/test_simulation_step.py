if __name__ == '__main__':
    import context

import genetic.simulators as simulators
import genetic.learners as learners

import unittest

class highest_id_wins(simulators.Component):

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def start_member(self, member):
        member.configuration.test = member.id

    def contest_members(self, contestant1, contestant2, result):
        if contestant1.id > contestant2.id:
            result.decisive(1)
        else:
            result.decisive(2)

class copy_mod_id_on_start(simulators.Component):

    def __init__(self, max):
        self.max = max

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("test", simulators.Dataset.Battle, [simulators.Role.Property])

    def start_member(self, member):
        member.configuration.test = member.id % self.max

class simulation_step_fixture(unittest.TestCase):

    def test_one_id_battle(self):
        # To get the ball rolling run one round of highest ID wins battle
        simulation = simulators.Simulation("Test", [highest_id_wins()], population_size=2)
        simulation.start()
        simulation.step()
        self.assertEqual(simulation.members[0].n_victory, 0)
        self.assertEqual(simulation.members[0].n_defeat, 1)
        self.assertEqual(len(simulation.members[0].contests), 1)
        self.assertEqual(simulation.members[1].n_victory, 1)
        self.assertEqual(simulation.members[1].n_defeat, 0)
        self.assertEqual(len(simulation.members[1].contests), 1)

    def test_step_count(self):
        simulation = simulators.Simulation("Test", [highest_id_wins()], population_size=2)
        simulation.start()
        sample_member = simulation.members[0]
        self.assertEqual(simulation.n_steps, 0)
        simulation.step()
        self.assertEqual(simulation.n_steps, 1)
        simulation.step()
        self.assertEqual(simulation.n_steps, 2)

    def test_step_count(self):
        simulation = simulators.Simulation("Test", [highest_id_wins()], population_size=2)
        simulation.start()
        sample_member = simulation.members[0]
        self.assertEqual(simulation.n_steps, 0)
        simulation.step()
        self.assertEqual(simulation.n_steps, 1)
        simulation.step()
        self.assertEqual(simulation.n_steps, 2)

    def test_contestants_report(self):
        simulation = simulators.Simulation("Test", [highest_id_wins()], population_size=2)
        simulation.start()
        simulation.step()
        member_ids = [simulation.members[0].id, simulation.members[1].id]
        self.assertTrue(len(simulation.reports) == 2)
        self.assertEqual(simulation.reports[0].step, 1)
        self.assertTrue(simulation.reports[0].member_id in member_ids)
        self.assertTrue(simulation.reports[1].member_id in member_ids)

    def test_reincarnations(self):
        # If we can only have one reincarnation after one round one member must have been on the reincarnation queue
        simulation = simulators.Simulation("Test", [copy_mod_id_on_start(1)], population_size=2)
        simulation.start()
        simulation.step()
        self.assertEqual(len(simulation.members), 1)
        self.assertEqual(len(simulation.reincarnations), 1)
        self.assertTrue(simulation.reincarnations[-1].dead)

if __name__ == '__main__':
    unittest.main()

