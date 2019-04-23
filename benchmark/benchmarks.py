# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters
import autem.evaluators as evaluators
import autem.makers as makers

import openml

import benchmark.utility as utility
import benchmark.baselines as baselines

import time
import datetime

from pathlib import Path

def get_study():
    return "LC1"

def get_simulations_path():
    return Path("benchmark/simulations")

def get_version():
    return 15

def make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, path, memory, max_time = None, properties = {}):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    version = get_version()
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

            workflows.Snapshot(max_time=max_time),

            baselines.BaselineStats(baseline_name),
            reporters.Path(path),
            hyper_learners.ClassificationSnapshot(),
        ], 
        seed = seed,
        n_jobs=6,
        identity = properties,
        memory=memory)
    return simulation

def run_benchmark_simulation(study, baseline_name):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    seed = 1
    max_time = 2 * 60 * 60
    path = get_simulations_path().joinpath(study).joinpath(experiment)
    memory = str(path.joinpath("cache"))

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, path, memory=memory)
    simulation.run()
    autem.ReportManager(path).update_combined_reports()

def run_benchmark_simulations(study = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    for baseline_name in baseline_names:
        run_benchmark_simulation(study, baseline_name)

def combine_reports(experiment, baseline):
    experiment_path = simulations_path().joinpath(experiment).joinpath(baseline)
    autem.ReportManager(experiment_path).update_combined_reports()

def combine_experiment_reports(experiment):
    experiment_path = simulations_path().joinpath(experiment)
    autem.ReportManager(experiment_path).update_combined_reports()
