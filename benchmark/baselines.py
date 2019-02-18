if __name__ == '__main__':
    import context

from benchmark.benchmark_common import *    
from pathlib import Path
import os
import csv
import pandas

# from benchmark.download_opemml_task import download_task_data

def baselines_path():
    return Path("benchmark/baselines")

def baseline_directory(baseline_name):
    return baselines_path().joinpath(baseline_name)

def baseline_data_filename(baseline_name):
    return baseline_directory(baseline_name).joinpath("baseline_data.csv")

def load_baseline_data(baseline_name):
    filename = baseline_data_filename(baseline_name)
    df = pandas.read_csv(filename)
    return df

if __name__ == '__main__':
    print(load_baseline_data("tic-tac-toe"))
