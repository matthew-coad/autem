if __name__ == '__main__':
    import context

import config

import openml
import os
from pathlib import Path
import warnings
import shutil

def data_path():
    return Path("benchmark/data")

def simulations_path():
    return Path("benchmark/simulations")

def full_benchmark_dids():
    return [11, 18, 23, 36, 37, 50, 54, 333, 334, 335, 375, 469, 1462, 1464, 1480, 1489, 40496, 40981]

def test_benchmark_dids():
    return [11, 18, 23]

def benchmark_dids():
    return full_benchmark_dids()

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')

def prepare_directory(path):
    if os.path.exists((path)):
        shutil.rmtree(path)
    if not os.path.exists(simulations_path()):
        os.mkdir(simulations_path())
    os.mkdir(path)

def prepare_experiment(path):
    warnings.filterwarnings("error")
    prepare_OpenML()
    prepare_directory(path)

def get_benchmark_data(did):
    dataset = openml.datasets.get_dataset(did)
    x, y = dataset.get_data(target=dataset.default_target_attribute)
    name = dataset.name
    return (name, x, y)

def run_simulation(simulation, epochs):
    simulation.start()
    for index in range(epochs):
        simulation.run(100)
        simulation.report()
        if not simulation.running:
            break
    return simulation