if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.selectors.classification as selectors
import genetic.learners.classification as learners
import genetic.transforms as transforms
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests

from benchmark.benchmark_common import *

experiment_name = "select"
population_size = 20
seed = 1
epochs = 5

def run_experiment_simulation(did, experiment_path):
    data_name, x, y = get_benchmark_data(did)
    simulation = simulators.Simulation(
        data_name, 
        [
            loaders.Data(data_name, x, y),
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
            reporters.Path(experiment_path)
        ], 
        population_size=population_size,
        seed = seed,
        properties= { "experiment": experiment_name })
    run_simulation(simulation, epochs)
    return simulation

def run_experiment():
    experiment_path = simulations_path().joinpath(experiment_name)
    prepare_experiment(experiment_path)
    for did in benchmark_dids():
        run_experiment_simulation(did, experiment_path)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_experiment()
