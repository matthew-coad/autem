from .simulation_info import SimulationInfo
from .utility import get_report_columns, get_report_frame

import pandas as pd
import os
import fnmatch
import shutil

def prepare_path(path):
    """
    Prepare the file system for a simulation reports
    """
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
    if not os.path.isdir(path):
        os.mkdir(path)


class ReportManager():
    """
    Simulation reports manager
    """
    def __init__(self, path):
        self.path = path

    def get_simulation(self, name):
        path = self.path.joinpath(name)
        simulation = SimulationInfo(name, path)
        return simulation

    def get_simulations(self):
        """
        List all available simulations
        """
        if not os.path.isdir(self.path):
            return []
        directories = [n for n in os.listdir(self.path) if os.path.isdir(self.path.joinpath(n))]
        simulations = [self.get_simulation(n) for n in directories]
        return simulations

    def prepare_simulation(self, simulation):
        prepare_path(simulation.path)

    def update_battle_report(self, simulation, report_id, frame):
        filename = "%s_%06d.csv" % ("Battle", report_id)
        full_path = simulation.path.joinpath(filename)
        frame.to_csv(full_path, index=False)

    def update_outline_report(self, simulation, frame):
        filename = "Outline.csv"
        full_path = simulation.path.joinpath(filename)
        frame.to_csv(full_path, index=False)

    def read_battle_report(self, simulation):
        """
        Read the battle report for a simulation
        """
        files = [simulation.path.joinpath(n) for n in os.listdir(simulation.path) if fnmatch.fnmatch(n, 'Battle_*.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames)
        return df
