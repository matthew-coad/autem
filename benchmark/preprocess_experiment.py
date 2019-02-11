if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.preprocessors as preprocessors
import genetic.learners.classification as learners
import genetic.transforms as transforms
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests

from benchmark.benchmark_common import *

experiment_name = "preprocess"

def run_preprocess_experiment(did, seed, experiment_path, epochs, population_size):
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

            preprocessors.Binarizer(),
            preprocessors.FastICA(),
            preprocessors.FeatureAgglomeration(), 
            preprocessors.MaxAbsScaler(), 
            preprocessors.MinMaxScaler(), 
            preprocessors.Normalizer(), 
            preprocessors.PCA(), 
            preprocessors.PolynomialFeatures(), 
            preprocessors.RBFSampler(),
            preprocessors.RobustScaler(), 
            preprocessors.StandardScaler(),

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
    run_simulation(simulation,  epochs)
    genetic.ReportManager(simulation_path).update_combined_reports()
    return simulation

def run_experiment():
    experiment_path = simulations_path().joinpath(experiment_name)
    prepare_experiment(experiment_path)
    dids = benchmark_dids()
    seeds = benchmark_seeds()
    epochs = benchmark_epochs()
    population_size = benchmark_population_size()

    for did in dids:
        for seed in seeds:
            run_preprocess_experiment(did, seed, experiment_path, epochs, population_size)
            genetic.ReportManager(simulations_path()).update_combined_reports()
            genetic.ReportManager(experiment_path).update_combined_reports()

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_experiment()
