if __name__ == '__main__':
    import context

import unittest

import genetic.simulators as simulators
import genetic.reporters as reporters
import genetic.reporters.utility as utility

class ReportMemory(reporters.Reporter):

    def __init__(self):
        reporters.Reporter.__init__(self, "report_member")
        self.step = None
        self.report = None

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        steps = simulation.n_steps
        records = simulation.reports
        frame = utility.get_report_frame(records)
        self.step = steps
        self.report = frame

class highest_id_wins(simulators.Component):

    def __init__(self):
        simulators.Component.__init__(self, "highest_id_wins")

    def prepare_member(self, member):
        member.configuration.test = member.id

    def contest_members(self, contestant1, contestant2, result):
        if contestant1.id > contestant2.id:
            result.decisive(1)
        else:
            result.decisive(2)

class test_reports_fixture(unittest.TestCase):

    def test_report_one_step(self):
        rm = ReportMemory()
        simulation = simulators.Simulation("Test", [highest_id_wins(), rm], population_size=2)
        simulation.start()
        simulation.step()
        simulation.report()
        self.assertIsNotNone(rm.report)
