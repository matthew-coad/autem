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
import genetic.evaluators as evaluators

import benchmark.utility as utility
import benchmark.baselines as baselines

from pathlib import Path

def simulations_path():
    return Path("benchmark/simulations")

def make_openml_light_classifier_simulation(name, task_id, seed, population_size, path, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    properties['dataset'] = dataset_name
    simulation = simulators.Simulation(
        name, 
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            evaluators.Accuracy(),
            evaluators.Survival(),
            evaluators.OpenMLRater(task_id),
            baselines.BaselineStats(name),
            evaluators.HoldoutValidator(),
            reporters.Path(path),

            # Imputers
            simulators.Choice("Imputer", [
                preprocessors.NoImputer(),
                preprocessors.SimpleImputer(),
                preprocessors.MissingIndicatorImputer(),
            ]),

            # Engineers
            simulators.Choice("Engineer", [
                preprocessors.NoEngineering(),
                preprocessors.PolynomialFeatures(),
            ]),

            # Scalers
            simulators.Choice("Scaler", [
                preprocessors.NoScaler(),
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.Binarizer(),
            ]),

            # Feature Reducers
            simulators.Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
                preprocessors.SelectPercentile(),
            ]),

            # Approximators
            simulators.Choice("Approximator", [
                preprocessors.NoApproximator(),
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ]),

            simulators.Choice("Learner", [
                learners.GaussianNB(),
                learners.BernoulliNB(),
                learners.MultinomialNB(),
                learners.DecisionTreeClassifier(),
                learners.KNeighborsClassifier(),
                learners.LinearSVC(),
                learners.LogisticRegression(),
                learners.LinearDiscriminantAnalysis(),
                learners.RandomForestClassifier(),
                learners.ExtraTreesClassifier(),
            ]),
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

def run_test_simulation():
    name = "eucalyptus"
    task_id = baselines.get_baseline_configuration(name)
    seed = 1
    steps = 100
    epochs = 50
    population_size = 20
    path = simulations_path().joinpath(name).joinpath(str(task_id))

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(name, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)

def run_benchmark_simulation(baseline_name):
    task_id = baselines.get_baseline_configuration(baseline_name)
    name = baseline_name
    seed = 1
    epochs = 50
    steps = 100
    population_size = 20
    path = simulations_path().joinpath(name).joinpath(str(task_id))

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(name, task_id, seed, population_size, path)
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
    run_test_simulation()
