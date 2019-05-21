if __name__ == '__main__':
    import context

import benchmark.baselines

from pathlib import Path
import csv
import pandas
import numpy as np

def get_hyper_directory():
    return Path("hyper")

def get_baselines_directory():
    return benchmark.baselines.baselines_directory()

def get_hyper_configuration_filename():
    return get_hyper_directory().joinpath("Configuration.xlsx")

def get_hyper_simulations_path():
    return get_hyper_directory().joinpath("Simulations")

def load_hyper_configuration_data():
    filename = get_hyper_configuration_filename()
    df = pandas.read_excel(filename)
    return df

def get_hyper_names(status = "Run"):
    df = load_hyper_configuration_data()
    dfa = df[df["Status"] == status]
    return dfa.Name

def get_hyper_configuration(name):
    df = load_hyper_configuration_data()
    dfa = df[df['Name'] == name]
    configuration = dfa.to_dict('records')[0]
    return configuration

if __name__ == '__main__':
    print(get_hyper_configuration("diabetes"))
