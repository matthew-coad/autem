# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters

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

def make_snapshot_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationSnapshot(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

def make_ensemble_snapshot_simulation(name, identity, data_id, max_time, n_jobs, seed, path, memory):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            baselines.BaselineStats(identity['dataset']),
            hyper_learners.ClassificationEnsemble(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

simulation_builders = {
    'snapshot': make_snapshot_simulation,
    'ensemble_snapshot': make_ensemble_snapshot_simulation,
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

