from ..simulation_manager import SimulationManager
from .reporter import Reporter
from .report_manager import ReportManager

import os

class Csv(Reporter, SimulationManager):

    def __init__(self, path):
        Reporter.__init__(self)
        self.path = path
        self.manager = ReportManager(self.path)

    def get_simulation_info(self, simulation):
        simulation_info = self.manager.get_simulation(self.path)
        return simulation_info

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        report_id = simulation.get_current_specie().get_current_epoch_id()
        battle_frame = self.get_battle_frame(simulation)
        simulation_info = self.get_simulation_info(simulation)
        if not battle_frame is None:
            self.manager.update_battle_report(simulation_info, report_id, battle_frame)

    def prepare_simulation(self, simulation):
        simulation_info = self.get_simulation_info(simulation)
        self.manager.prepare_simulation(simulation_info)
        outline_frame = self.get_outline_frame(simulation)
        self.manager.update_outline_report(simulation_info, outline_frame)

    def finish_simulation(self, simulation):
        self.manager.update_combined_reports()
