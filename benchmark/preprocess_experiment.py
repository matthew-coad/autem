if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.preprocessors as preprocessors
import genetic.learners.classification as learners
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests

from benchmark.benchmark_common import *

from openML_rater import OpenMLRater

experiment_name = "preprocess"

def run_preprocess_experiment(did, task_id, seed, experiment_path, epochs, population_size):
    data_name, x, y = get_benchmark_data(did)
    simulation_path = experiment_path.joinpath(data_name)
    simulation = simulators.Simulation(
        data_name, 
        [
            loaders.Data(data_name, x, y),
            scorers.Accuracy(),

            contests.BestLearner(),
            contests.Survival(),
            OpenMLRater(task_id),
            reporters.Path(simulation_path),

            # Engineers
            preprocessors.NoEngineering(),
            preprocessors.PolynomialFeatures(),

            # Scalers
            preprocessors.NoScaler(),
            preprocessors.MaxAbsScaler(),
            preprocessors.MinMaxScaler(),
            preprocessors.Normalizer(),
            preprocessors.RobustScaler(),
            preprocessors.StandardScaler(),
            preprocessors.Binarizer(),

            # Feature Reducers
            preprocessors.NoReducer(),
            preprocessors.FastICA(),
            preprocessors.FeatureAgglomeration(),
            preprocessors.PCA(),
            preprocessors.SelectPercentile(),

            # Approximators
            preprocessors.NoApproximator(),
            preprocessors.RBFSampler(),
            preprocessors.Nystroem(),

            learners.GaussianNB(),
            learners.BernoulliNB(),
            learners.MultinomialNB(),
            learners.DecisionTreeClassifier(),
            learners.KNeighborsClassifier(),
            learners.LinearSVC(),
            learners.LogisticRegression(),
            learners.LinearDiscriminantAnalysis(),

            # learners.ExtraTreesClassifier(),
            #learners.RandomForestClassifier(),
            # learners.GradientBoostingClassifier(),
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

    # EEG eye state: data_id:1471, task_id:14951
    did = 1471
    task_id = 14951
    seeds = benchmark_seeds()
    population_size = benchmark_population_size()
    epochs = benchmark_epochs()

    run_preprocess_experiment(did, task_id, seeds[0], experiment_path, epochs, population_size)

#    for did in dids:
#        run_preprocess_experiment(did, seeds[0], experiment_path, epochs, population_size)
#        genetic.ReportManager(simulations_path()).update_combined_reports()
#        genetic.ReportManager(experiment_path).update_combined_reports()

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_experiment()
