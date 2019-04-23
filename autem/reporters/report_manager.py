from .utility import get_report_columns, get_report_frame

import pandas as pd
import os
import fnmatch
import shutil
import pathlib

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
        os.makedirs(path)

class SimulationInfo:

    """
    Information about a simulation that is useful to reporting
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path        

class ReportManager():
    """
    Simulation reports manager
    """
    def __init__(self, path):
        self.path = path

    def get_simulation(self, path):
        name = os.path.basename(path)
        simulation = SimulationInfo(name, path)
        return simulation

    def get_simulations(self):
        """
        List all available simulations
        """
        directories = [root for root, dir, files in os.walk(self.path) if any(fnmatch.filter(files, "outline.csv"))]
        simulations = [self.get_simulation(pathlib.Path(n)) for n in directories]
        return simulations

    def prepare_simulation(self, simulation):
        prepare_path(self.path)

    def update_battle_report(self, simulation, report_id, frame):
        filename = "%s_%06d.csv" % ("Battle", report_id)
        full_path = self.path.joinpath(filename)
        frame.to_csv(full_path, index=False)

    def update_outline_report(self, simulation, frame):
        filename = "Outline.csv"
        full_path = self.path.joinpath(filename)
        frame.to_csv(full_path, index=False)

    def read_battle_report(self, simulation):
        """
        Read the battle report for a simulation
        """
        files = [self.path(n) for n in os.listdir(self.path) if fnmatch.fnmatch(n, 'Battle_*.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames)
        return df

    def read_combined_battle_report(self):
        """
        Combine all battle reports into one frame
        """
        simulations = self.get_simulations()
        files = [s.path.joinpath(n) for s in simulations for n in os.listdir(s.path) if fnmatch.fnmatch(n, 'Battle_*.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames, sort=False)
        return df

    def update_combined_battle_report(self):
        frame = self.read_combined_battle_report()
        full_path = self.path.joinpath("Battle.csv")
        frame.to_csv(full_path, index=False)

    def read_combined_outline_report(self):
        """
        Combine all outline reports into one frame
        """
        simulations = self.get_simulations()
        files = [s.path.joinpath(n) for s in simulations for n in os.listdir(s.path) if fnmatch.fnmatch(n, 'Outline.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames, ignore_index=True).drop_duplicates().reset_index(drop=True)
        return df

    def update_combined_outline_report(self):
        frame = self.read_combined_outline_report()
        full_path = self.path.joinpath("Outline.csv")
        frame.to_csv(full_path, index=False)

    def update_combined_reports(self):
        self.update_combined_outline_report()
        self.update_combined_battle_report()
