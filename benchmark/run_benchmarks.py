if __name__ == '__main__':
    import context

import openml

import autem
import autem.scorers as scorers
import autem.preprocessors as preprocessors
import autem.learners.classification as learners
import autem.loaders as loaders
import autem.reporters as reporters
import autem.evaluators as evaluators

import benchmark.utility as utility
import benchmark.baselines as baselines

from pathlib import Path

def simulations_path():
    return Path("benchmark/simulations")

version = 4

def make_openml_tune_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "%s_%s_v%d" % (experiment, baseline_name, version)
    properties['dataset'] = dataset_name
    properties['experiment'] = experiment
    properties['version'] = version
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            evaluators.AccuracyContest(),
            evaluators.Survival(),
            evaluators.OpenMLRater(task_id),
            baselines.BaselineStats(baseline_name),
            evaluators.HoldoutValidator(),
            reporters.Path(path),

            # Imputers
            preprocessors.SimpleImputer([]),

            # Scalers
            preprocessors.Normalizer({}),
            preprocessors.StandardScaler(),

            autem.Choice("Learner", [
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

def make_openml_light_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "%s_%s_v%d" % (experiment, baseline_name, version)
    properties['dataset'] = dataset_name
    properties['experiment'] = experiment
    properties['version'] = version
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            evaluators.AccuracyContest(),
            evaluators.DurationContest(),

            evaluators.Survival(),
            evaluators.OpenMLRater(task_id),
            baselines.BaselineStats(baseline_name),
            evaluators.HoldoutValidator(),
            reporters.Path(path),

            # Imputers
            autem.Choice("Imputer", [
                preprocessors.SimpleImputer(),
            ], preprocessors.NoImputer()),

            # Engineers
            autem.Choice("Engineer", [
                preprocessors.PolynomialFeatures(),
            ], preprocessors.NoEngineering()),

            # Scalers
            autem.Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.Binarizer(),
                preprocessors.BoxCoxTransform(),
                preprocessors.YeoJohnsonTransform()
            ], preprocessors.NoScaler()),

            # Feature Reducers
            autem.Choice("Reducer", [
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
                preprocessors.SelectPercentile(),
            ], preprocessors.NoReducer()),

            # Approximators
            autem.Choice("Approximator", [
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ], preprocessors.NoApproximator()),

            autem.Choice("Learner", [
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

def make_openml_classifier_simulation(configuration, baseline_name, experiment, task_id, seed, population_size, path, properties = {}):
    if configuration == "Light":
        return make_openml_light_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties)
    elif configuration == "LightX":
        return make_openml_lightx_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties)
    elif configuration == "Tune":
        return make_openml_tune_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties)
    elif configuration == "Select":
        return make_openml_select_classifier_simulation(baseline_name, experiment, task_id, seed, population_size, path, properties)
    raise RuntimeError("Unknown configuration")


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
    baseline_name = "vehicle"
    configuation = "Light"
    experiment = "Test_Light"
    configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = configuration["task_id"]
    seed = 1
    steps = 100
    epochs = 40
    population_size = 20
    path = simulations_path().joinpath("test").joinpath(str(experiment)).joinpath(baseline_name)

    utility.prepare_OpenML()
    simulation = make_openml_classifier_simulation(configuation, baseline_name, experiment, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)

def run_benchmark_simulation(configuration, baseline_name, experiment):
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    seed = 1
    epochs = 40
    steps = 100
    population_size = 20
    path = simulations_path().joinpath("Run").joinpath(str(experiment)).joinpath(baseline_name)

    utility.prepare_OpenML()
    simulation = make_openml_classifier_simulation(configuration, baseline_name, experiment, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)
    autem.ReportManager(path).update_combined_reports()

def run_benchmark_simulations(configurations):
    baseline_names = baselines.get_baseline_names("Select")
    for baseline_name in baseline_names:
        for configuration in configurations:
            run_benchmark_simulation(configuration, baseline_name, configuration)

def combine_reports(experiment, baseline):
    experiment_path = simulations_path().joinpath(experiment).joinpath(baseline)
    autem.ReportManager(experiment_path).update_combined_reports()

def combine_experiment_reports(experiment):
    experiment_path = simulations_path().joinpath(experiment)
    autem.ReportManager(experiment_path).update_combined_reports()

import warnings
import sklearn.exceptions

if __name__ == '__main__':
    run_benchmark_simulations(["Light"])
    # run_test_simulation()
