if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.preprocessors as preprocessors
import autem.learners.classification as learners
import autem.loaders as loaders
import autem.reporters as reporters
import autem.evaluators as evaluators

import openml

import benchmark.utility as utility
import benchmark.baselines as baselines

from pathlib import Path

def simulations_path():
    return Path("benchmark/simulations")

study = "leagues"
version = 9

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
            evaluators.ContestSurvival(),
            evaluators.CrossValidationRater(),
            evaluators.OpenMLRater(task_id),
            evaluators.DummyClassifierAccuracy(),
            evaluators.ValidationAccuracy(),
            BenchmarkScorer(),

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

def make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "%s_%s_v%d" % (study, experiment, version)
    properties['study'] = study
    properties['experiment'] = experiment
    properties['dataset'] = dataset_name
    properties['version'] = version
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),

            evaluators.AccuracyContest(),
            evaluators.ContestSurvival(),
            evaluators.CrossValidationRater(),
            evaluators.OpenMLRater(task_id),
            evaluators.DummyClassifierAccuracy(),
            evaluators.ValidationAccuracy(),
            baselines.BaselineStats(baseline_name),

            reporters.Path(path),

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
            ]),

            # Feature Selectors
            autem.Choice("Selector", [
                preprocessors.NoSelector(),
                preprocessors.SelectPercentile(),
                preprocessors.VarianceThreshold()
            ]),

            # Feature Reducers
            autem.Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
            ]),

            # Approximators
            autem.Choice("Approximator", [
                preprocessors.NoApproximator(),
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ]),

            autem.Choice("Learner", [
                learners.GaussianNB(),
                learners.BernoulliNB(),
                learners.MultinomialNB(),
                learners.DecisionTreeClassifier(),
                learners.KNeighborsClassifier(),
                learners.LinearSVC(),
                # learners.RadialBasisSVC(),
                # learners.PolySVC(),
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
    baseline_name = "vehicle"
    experiment = baseline_name
    configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = configuration["task_id"]
    seed = 1
    steps = 100
    epochs = 2
    population_size = 20
    path = simulations_path().joinpath("test").joinpath(study).joinpath(baseline_name)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)
    autem.ReportManager(path).update_combined_reports()

def run_benchmark_simulation(baseline_name):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    seed = 1
    epochs = 50
    steps = 100
    population_size = 20
    path = simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path)
    run_simulation(simulation, steps, epochs)
    autem.ReportManager(path).update_combined_reports()

def run_benchmark_simulations():
    baseline_names = baselines.get_baseline_names("Select")
    for baseline_name in baseline_names:
        run_benchmark_simulation(baseline_name)

def combine_reports(experiment, baseline):
    experiment_path = simulations_path().joinpath(experiment).joinpath(baseline)
    autem.ReportManager(experiment_path).update_combined_reports()

def combine_experiment_reports(experiment):
    experiment_path = simulations_path().joinpath(experiment)
    autem.ReportManager(experiment_path).update_combined_reports()

if __name__ == '__main__':
    run_test_simulation()
    #run_benchmark_simulations()
