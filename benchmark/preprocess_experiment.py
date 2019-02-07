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
population_size = 20
seed = 1
epochs = 40

def run_preprocess_experiment(did, experiment_path):
    data_name, x, y = get_benchmark_data(did)
    simulation = simulators.Simulation(
        data_name, 
        [
            loaders.Data(data_name, x, y),
            scorers.Accuracy(),

            contests.BestLearner(), 
            contests.Survival(),
            reporters.Path(experiment_path),

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
        properties= { "experiment": experiment_name })
    run_simulation(simulation, epochs)
    return simulation

def run_experiment():
    experiment_path = simulations_path().joinpath(experiment_name)
    prepare_experiment(experiment_path)
    dids = benchmark_dids()
    for did in dids:
        run_preprocess_experiment(did, experiment_path)
        genetic.ReportManager(simulations_path()).update_combined_reports()
        genetic.ReportManager(experiment_path).update_combined_reports()

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_experiment()
