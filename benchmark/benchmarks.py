# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.learners.classification as learners
import autem.preprocessors as preprocessors
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters
import autem.validators as validators

import openml

import benchmark.utility as utility
import benchmark.baselines as baselines

import time
import datetime

from pathlib import Path

def get_study():
    return "PP2"

def get_simulations_path():
    return Path("benchmark/simulations")

def get_version():
    return 15

def get_n_jobs():
    return 4

# Baseline configurations

def make_snapshot_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationSnapshot(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_hammer_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(max_time=max_time, max_species=3),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationBaseline(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_mastery_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Mastery([ "Learner" ]),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationBaseline(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

# Linear configurations

def make_linear_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationLinear(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_linear_short_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationLinear(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_linear_mastery_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Mastery([ "Learner" ]),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationLinear(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation


# Trees configurations

def make_trees_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationTrees(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_trees_short_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationTrees(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation


def make_trees_mastery_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Mastery([ "Learner" ]),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationTrees(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

# SVM configurations    

def make_svm_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationSVM(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_svm_short_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationSVM(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_svm_mastery_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Mastery([ "Learner" ]),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationSVM(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_xgb_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),

            # Scalers
            autem.Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.BoxCoxTransform(),
                preprocessors.YeoJohnsonTransform(),
            ]),

            # Feature Selectors
            autem.Choice("Selector", [
                preprocessors.NoSelector(),
            ]),

            # Feature Reducers
            autem.Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.FastICA(),
                preprocessors.PCA(),
            ]),

            # Approximators
            autem.Choice("Approximator", [
                preprocessors.NoApproximator(),
            ]),

            autem.Choice("Learner", [
                learners.XGBClassifier(),
            ]),

            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

simulation_builders = {
    'snapshot': make_snapshot_simulation,
    'hammer': make_hammer_simulation,
    'mastery': make_mastery_simulation,

    'linear': make_linear_simulation,
    'short_linear': make_short_linear_simulation,

    'trees': make_trees_simulation,
    'trees_short': make_trees_short_simulation,
    'trees_mastery': make_trees_mastery_simulation,

    'svm': make_svm_simulation,
    'svm_short': make_svm_short_simulation,
    'svm_mastery': make_svm_mastery_simulation,

    'xgb': make_xgb_simulation,

}

def run_benchmark_simulation(study, baseline_name):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    version = get_version()

    configuration = baseline_configuration["Configuration"]
    configuration_valid = configuration in simulation_builders
    if not configuration_valid:
        print("Baseline %s configuration %s does not exist" % (baseline_name, configuration))
        return None

    name = "'%s_%s_%s v%d'" % (study, experiment, configuration, version)
    identity = {
        'study': study,
        'experiment': experiment,
        'dataset': baseline_name,
        'version': version,
        'configuration': configuration,
    }    

    max_time = 2 * 60 * 60
    n_jobs = get_n_jobs()
    seed = 1
    path = get_simulations_path().joinpath(study).joinpath(experiment)
    memory = str(path.joinpath("cache"))

    utility.prepare_OpenML()
    simulation_builder = simulation_builders[configuration]
    simulation = simulation_builder(name, identity, data_id, max_time, n_jobs, seed, path, memory)
    simulation.run()

def run_benchmark_simulations(study = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    for baseline_name in baseline_names:
        run_benchmark_simulation(study, baseline_name)

