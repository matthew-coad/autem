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
    return "SN1"

def get_simulations_path():
    return Path("benchmark/simulations")

def get_version():
    return 15

def get_n_jobs():
    return 4

def make_snapshot_simulation(study, experiment, baseline_name, data_id, max_time, version, n_jobs, seed):
    configuration = "snapshot"
    name = "%s_%s_v%d %s" % (study, experiment, version, configuration)
    path = get_simulations_path().joinpath(study).joinpath(experiment)
    memory = str(path.joinpath("cache"))

    identity = {
        'study': study,
        'experiment': experiment,
        'dataset': baseline_name,
        'version': version,
        'configuration': configuration,
    }    

    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            baselines.BaselineStats(baseline_name),
            hyper_learners.ClassificationSnapshot(),
            reporters.Csv(path),
        ], 
        seed = seed, n_jobs=n_jobs, identity=identity, memory=memory)
    return simulation

simulation_builders = {
    'snapshot': make_snapshot_simulation,
}

def run_benchmark_simulation(study, baseline_name):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    configuration = baseline_configuration["Configuration"]
    configuration_valid = configuration in simulation_builders
    if not configuration_valid:
        print("Baseline %s configuration %s does not exist" % (baseline_name, configuration))
        return None

    max_time = 2 * 60 * 60
    version = get_version()
    n_jobs = get_n_jobs()
    seed = 1

    utility.prepare_OpenML()
    simulation_builder = simulation_builders[configuration]
    simulation = simulation_builder(study, experiment, baseline_name, data_id, max_time, version, n_jobs, seed)
    simulation.run()

def run_benchmark_simulations(study = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    for baseline_name in baseline_names:
        run_benchmark_simulation(study, baseline_name)

