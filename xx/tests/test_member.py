if __name__ == '__main__':
    import context

import autem.simulators as simulators

import unittest


class member_fixture(unittest.TestCase):

    def test_report_member_id(self):
        simulation = simulators.Simulation("Test", [], population_size=3)
        simulation.start()
        for member in simulation.members:
            record = simulation.record_member(member)
            self.assertEqual(record.member_id, member.id)

if __name__ == '__main__':
    unittest.main()
