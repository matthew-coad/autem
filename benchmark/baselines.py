if __name__ == '__main__':
    import context

from genetic.evaluators import Evaluater

from benchmark.benchmark_common import *    
from pathlib import Path
import os
import csv
import pandas
import numpy as np

# from benchmark.download_opemml_task import download_task_data

def baselines_directory():
    return Path("benchmark/baselines")

def baseline_configuration_filename():
    return baselines_directory().joinpath("configuration.csv")

def load_baseline_configuration_data():
    filename = baseline_configuration_filename()
    df = pandas.read_csv(filename)
    return df

def get_baseline_names():
    df = load_baseline_configuration_data()
    return df.name

def get_baseline_configuration(name):
    df = load_baseline_configuration_data()
    dfa = df[df['name'] == name]
    task_id = list(dfa.task_id)[0]
    return (task_id)

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

class BaselineRater(Evaluater):

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

    def rate_member(self, member):
        simulation = member.simulation
        stats = simulation.resources.baseline_stats

        member.ratings.top_accuracy = stats["max_score"]
        member.ratings.top_1p_accuracy = stats["top_1p"]
        member.ratings.top_5p_accuracy = stats["top_5p"]
        member.ratings.top_10p_accuracy = stats["top_10p"]
        member.ratings.top_25p_accuracy = stats["top_qtr"]

    def record_member(self, member, record):

        if hasattr(member.ratings, "top_accuracy"):
            record.top_accuracy = member.ratings.top_accuracy
            record.top_1p_accuracy = member.ratings.top_1p_accuracy
            record.top_5p_accuracy = member.ratings.top_5p_accuracy
            record.top_10p_accuracy = member.ratings.top_10p_accuracy
            record.top_25p_accuracy = member.ratings.top_25p_accuracy
        else:
            record.top_accuracy = None
            record.top_1p_accuracy = None
            record.top_5p_accuracy = None
            record.top_10p_accuracy = None
            record.top_25p_accuracy = None

if __name__ == '__main__':
    print(get_baseline_stats("tic-tac-toe"))

