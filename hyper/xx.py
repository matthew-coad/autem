import os
from pathlib import Path
import shutil

import config
import openml

def benchmark_directory():
    return Path("benchmark")

def prepare_experiment_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)        

def prepare_cache_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')


def configuration_filename():
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
