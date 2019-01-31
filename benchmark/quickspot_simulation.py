if __name__ == '__main__':
    import context

import config
import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.selectors.classification as selectors
import genetic.learners.classification as learners
import genetic.transforms as transforms
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests

import openml
import os
from pathlib import Path
import warnings

def data_path():
    return Path("benchmark/data")

def simulations_path():
    return Path("benchmark/simulations")

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')

def run_quick_spot_simulation(bid, seed):
    prepare_OpenML()
    dataset = openml.datasets.get_dataset(bid)
    x, y, attribute_names = dataset.get_data(target=dataset.default_target_attribute, return_attribute_names=True,)
    simulation_name = "%s_%d_select" % (dataset.name, seed)

    simulation = simulators.Simulation(
        simulation_name, 
        [
            loaders.Data(x,y),
            scorers.Accuracy(),

            learners.LogisticRegression(), 
            learners.LinearDiscriminantAnalysis(), 
            learners.KNeighborsClassifier(),  
            learners.DecisionTreeClassifier(), 
            learners.GaussianNB(), 
            learners.SVC(),

            selectors.SelectPercentile(),

            contests.BestLearner(), 
            contests.Survival(),
            reporters.Path(simulations_path())
        ], 
        population_size=20,
        seed = seed)
    simulation.start()
    for index in range(10):
        simulation.run(100)
        simulation.report()
        if not simulation.running:
            break
    return simulation

if __name__ == '__main__':
    dids = [11, 18, 23, 36, 37, 50, 54, 333, 334, 335, 375, 469, 1462, 1464, 1480, 1489, 40496, 40981]
    dids = [11]
    for did in dids:
        run_quick_spot_simulation(11, 1)
