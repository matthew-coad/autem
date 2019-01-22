from .reporter import Reporter
from .report_manager import ReportManager

class Path(Reporter):

    def __init__(self, path):
        self.path = path

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        steps = simulation.n_steps
        records = simulation.reports
        manager = ReportManager(self.path)
        simulation_info = manager.get_simulation(simulation.name)
        manager.update_battle_report(simulation_info, steps, records)
        
