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

experiment_name = "baseline"
population_size = 20
seed = 1
epochs = 40

def run_baseline_simulation(did, seed, experiment_path):
    data_name, x, y = get_benchmark_data(did)
    simulation_path = experiment_path.joinpath(data_name).joinpath(str(seed))
    simulation = simulators.Simulation(
        data_name, 
        [
            loaders.Data(data_name, x, y),
            scorers.Accuracy(),

            contests.BestLearner(), 
            contests.Survival(),
            reporters.Path(simulation_path),

            learners.GaussianNB(),
            learners.BernoulliNB(),
            learners.MultinomialNB(),
            learners.DecisionTreeClassifier(),
            learners.KNeighborsClassifier(),
            learners.LinearSVC(),
            learners.LogisticRegression(),
            learners.LinearDiscriminantAnalysis(),
        ], 
        population_size=population_size,
        seed = seed,
        properties= { "experiment": experiment_name, "seed": seed })
    run_simulation(simulation, epochs)
    genetic.ReportManager(simulation_path).update_combined_reports()
    return simulation

def run_experiment():
    experiment_path = simulations_path().joinpath(experiment_name)
    prepare_experiment(experiment_path)
    dids = benchmark_dids()
    seeds = benchmark_seeds()
    for did in dids:
        for seed in seeds:
            run_baseline_simulation(did, seed, experiment_path)
            genetic.ReportManager(simulations_path()).update_combined_reports()
            genetic.ReportManager(experiment_path).update_combined_reports()

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_experiment()
