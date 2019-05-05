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
    return "SP1"

def get_simulations_path():
    return Path("benchmark/simulations")

def get_version():
    return 15

def get_n_jobs():
    return 4

# Learners

learner_builders = {
    'baseline': hyper_learners.ClassificationBaseline,
    'linear': hyper_learners.ClassificationLinear,
    'trees': hyper_learners.ClassificationTrees,
    'svm': hyper_learners.ClassificationLinear,
}

# Baseline configurations

def make_spotcheck_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.SpotcheckWorkflow(),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation


def make_snapshot_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.SnapshotWorkflow(),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation

def make_hammer_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    settings = autem.SimulationSettings(simulation)
    settings.set_max_species(3)
    return simulation

def make_short_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Standard(),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation

def make_mastery_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Mastery([ "Learner" ]),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation

simulation_builders = {
    'spotcheck': make_spotcheck_simulation,
    'snapshot': make_snapshot_simulation,
    'hammer': make_hammer_simulation,
    'short': make_short_simulation,
    'mastery': make_mastery_simulation,
}

def run_benchmark_simulation(study, baseline_name, configuration = None, learner = None):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    version = get_version()

    configuration = baseline_configuration["Configuration"] if configuration is None else configuration
    learner = baseline_configuration["Learner"] if learner is None else learner
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
    simulation = simulation_builder(name, identity, data_id, learner, path)
    settings = autem.SimulationSettings(simulation)
    settings.set_identity(identity)
    settings.set_n_jobs(4)
    settings.set_seed(seed)
    settings.set_memory(memory)
    settings.set_max_time(max_time)

    simulation.run()

def run_benchmark_simulations(study = None, configuration = None, learner = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    for baseline_name in baseline_names:
        run_benchmark_simulation(study, baseline_name, configuration, learner)
