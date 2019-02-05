from .reporter import Reporter
import os

class Path(Reporter):

    def __init__(self, path):
        from genetic import ReportManager
        Reporter.__init__(self, "Path")
        self.path = path
        self.manager = ReportManager(self.path)

    def get_simulation_info(self, simulation):
        simulation_path = self.path.joinpath(simulation.name)
        simulation_info = self.manager.get_simulation(simulation_path)
        return simulation_info

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        report_id = simulation.n_steps
        battle_frame = self.get_battle_frame(simulation)
        ranking_frame = self.get_ranking_frame(simulation)
        simulation_info = self.get_simulation_info(simulation)
        if not battle_frame is None:
            self.manager.update_battle_report(simulation_info, report_id, battle_frame)
        if not ranking_frame is None:
            self.manager.update_ranking_report(simulation_info, report_id, ranking_frame)


    def start_simulation(self, simulation):
        simulation_info = self.get_simulation_info(simulation)
        self.manager.prepare_simulation(simulation_info)
        outline_frame = self.get_outline_frame(simulation)
        self.manager.update_outline_report(simulation_info, outline_frame)
