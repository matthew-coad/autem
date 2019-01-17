from . import populations

import pandas as pd
import os
import fnmatch
import shutil

class ReportManager():
    """
    Report service manager
    """
    def __init__(self, path):
        self.path = path

    def read_population_report(self):
        """
        Read the combined population report from a given path
        """
        files = [self.path.joinpath(n) for n in os.listdir(self.path) if fnmatch.fnmatch(n, 'Population_*.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames)
        return df

    def read_member_report(self):
        """
        Read the combined member report from a given path
        """
        files = [self.path.joinpath(n) for n in os.listdir(self.path) if fnmatch.fnmatch(n, 'Member_*.csv')]
        frames = [pd.read_csv(n) for n in files]
        df = pd.concat(frames, sort=True)
        return df
