if __name__ == '__main__':
    import context

from autem.evaluators import Evaluater

from benchmark.utility import *    
from pathlib import Path
import os
import csv
import pandas
import numpy as np

# from benchmark.download_opemml_task import download_task_data

def baselines_directory():
    return Path("benchmark/baselines")

def baseline_configuration_filename():
    return benchmark_directory().joinpath("Configuration.xlsx")

def load_baseline_configuration_data():
    filename = baseline_configuration_filename()
    df = pandas.read_excel(filename)
    return df

def get_baseline_names(experiment, status = "Run"):
    df = load_baseline_configuration_data()
    dfa = df[df[experiment] == status]
    return dfa.Name

def get_baseline_configuration(name):
    df = load_baseline_configuration_data()
    dfa = df[df['Name'] == name]
    configuration = dfa.to_dict('records')[0]
    return configuration

def baseline_directory(baseline_name):
    return baselines_directory().joinpath(baseline_name)

def baseline_data_filename(baseline_name):
    return baseline_directory(baseline_name).joinpath("baseline.csv")

def load_baseline_data(baseline_name):
    filename = baseline_data_filename(baseline_name)
    df = pandas.read_csv(filename)
    return df

def get_baseline_stats(baseline_name):
    df = load_baseline_data(baseline_name)
    n_runs = df.shape[0]
    scores = df.predictive_accuracy
    median_score = np.median(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)
    top_1p = np.percentile(scores, 99)
    top_5p = np.percentile(scores, 95)
    top_10p = np.percentile(scores, 90)
    top_qtr = np.percentile(scores, 75)

    stats = {
        "n_runs": n_runs,
        "median_score": median_score,
        "max_score": max_score,
        "min_score": min_score,
        "top_1p": top_1p,
        "top_5p": top_5p,
        "top_10p": top_10p,
        "top_qtr": top_qtr
    }
    return stats

class BaselineStats(Evaluater):

    """
    Rater that reports on the members baseline
    """

    def __init__(self, baseline_name):
        self.baseline_name = baseline_name

    def start_simulation(self, simulation):
        super().start_simulation(simulation)

        baseline_name = self.baseline_name
        stats = get_baseline_stats(baseline_name)
        simulation.resources.baseline_stats = stats

    def record_member(self, member, record):

        simulation = member.simulation
        stats = simulation.resources.baseline_stats

        record.BL_top_score = stats["max_score"]
        record.BL_top_5p_score = stats["top_5p"]

if __name__ == '__main__':
    names = get_baseline_names("Select")
    for name in names:
        print(get_baseline_stats(name))

