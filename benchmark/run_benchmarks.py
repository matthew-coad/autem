if __name__ == '__main__':
    import context

import openml

import genetic
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

version = 2

def make_openml_light_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "%s_%s_v%d" % (experiment, baseline_name, version)
    properties['dataset'] = dataset_name
    properties['experiment'] = experiment
    properties['version'] = version
    
    simulation = genetic.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            evaluators.Accuracy(),
            evaluators.Survival(),
            evaluators.OpenMLRater(task_id),
            baselines.BaselineStats(baseline_name),
            evaluators.HoldoutValidator(),
            evaluators.PreferImportantChoices(),
            reporters.Path(path),

            # Imputers
            genetic.Choice("Imputer", [
                preprocessors.NoImputer(),
                preprocessors.SimpleImputer()
            ]),

            # Engineers
            genetic.Choice("Engineer", [
                preprocessors.PolynomialFeatures(),
            ], preprocessors.NoEngineering()),

            # Scalers
            genetic.Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.Binarizer(),
            ], preprocessors.NoScaler()),

            # Feature Reducers
            genetic.Choice("Reducer", [
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
                preprocessors.SelectPercentile(),
            ], preprocessors.NoReducer()),

            # Approximators
            genetic.Choice("Approximator", [
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ], preprocessors.NoApproximator()),

            genetic.Choice("Learner", [
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
    print("Running %s" % simulation.name)
    simulation.start()
    for index in range(epochs):
        simulation.run(steps)
        if index == epochs - 1 or not simulation.running:
            simulation.finish()
        simulation.report()
        if not simulation.running:
            break

def run_test_simulation():
    baseline_name = "diabetes"
    experiment = "Run_Light"
    configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = configuration["task_id"]
    seed = 1
    steps = 100
    epochs = 40
    population_size = 20
    path = simulations_path().joinpath("test").joinpath(str(experiment)).joinpath(baseline_name)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)

def run_benchmark_simulation(baseline_name, experiment):
    configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = configuration["task_id"]
    seed = 1
    epochs = 40
    steps = 100
    population_size = 20
    path = simulations_path().joinpath(str(experiment)).joinpath(baseline_name)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)


def run_benchmark_simulations(experiment):
    baseline_names = baselines.get_baseline_names(experiment)
    for baseline_name in baseline_names:
        run_benchmark_simulation(baseline_name, experiment)

def combine_reports():
    experiment_path = simulations_path().joinpath(experiment_name)
    genetic.ReportManager(simulations_path()).update_combined_reports()
    genetic.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_test_simulation()
