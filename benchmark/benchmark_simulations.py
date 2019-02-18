if __name__ == '__main__':
    import context


import openml

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.preprocessors as preprocessors
import genetic.learners.classification as learners
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests
import genetic.raters as raters

import benchmark.utility as utility
import benchmark.baselines as baselines

from pathlib import Path

def simulations_path():
    return Path("benchmark/simulations")

def make_openml_light_classifier_simulation(name, data_id, task_id, seed, population_size, path, properties = {}):
    simulation = simulators.Simulation(
        name, 
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            contests.BestLearner(),
            contests.Survival(),
            raters.OpenMLRater(task_id),
            baselines.BaselineRater(name),
            raters.HoldoutValidator(),
            reporters.Path(path),

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
        ], 
        population_size = population_size,
        seed = seed,
        properties = properties)
    return simulation

def run_simulation(simulation, steps, epochs):
    simulation.start()
    for index in range(epochs):
        simulation.run(steps)
        if index == epochs - 1 or not simulation.running:
            simulation.finish()
        simulation.report()
        if not simulation.running:
            break

def run_tic_tac_toe():
    name = "tic-tac-toe"
    data_id, task_id = baselines.get_baseline_configuration(name)
    seed = 1
    steps = 100
    epochs = 20
    population_size = 20
    path = simulations_path().joinpath(name)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(name, data_id, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)

def run_benchmark_simulation(baseline_name):
    data_id, task_id = baselines.get_baseline_configuration(baseline_name)
    name = baseline_name
    seed = 1
    epochs = 40
    steps = 100
    population_size = 20
    path = simulations_path().joinpath(name)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(name, data_id, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)

def run_benchmark_simulations():
    baseline_names = baselines.get_baseline_names()
    for baseline_name in baseline_names:
        run_benchmark_simulation(baseline_name)

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_benchmark_simulations()
