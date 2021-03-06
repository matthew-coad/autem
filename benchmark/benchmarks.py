if __name__ == '__main__':
    import context

import autem
import autem.runners as runners
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
import multiprocessing

from pathlib import Path

def get_study():
    return "DGSC"

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
    'svm': hyper_learners.ClassificationSVM,
    'bayes': hyper_learners.ClassificationBayes,
    'wide': hyper_learners.ClassificationWide,
}

# Baseline configurations

def make_spotcheck_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
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
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.SnapshotWorkflow(),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation

def make_standard_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.StandardWorkflow(),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    settings = autem.SimulationSettings(simulation)
    settings.set_max_species(3)
    return simulation

def make_short_standard_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.StandardWorkflow(),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    settings = autem.SimulationSettings(simulation)
    settings.set_max_species(3)
    return simulation

def make_hammer_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.StandardWorkflow(max_species=3),
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
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.MasteryWorkflow(),
            validators.Holdout(0.2),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation

def make_short_mastery_simulation(name, identity, data_id, learner, path):
    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),            
            workflows.MasteryWorkflow(),
            baselines.BaselineStats(identity['dataset']),
            learner_builders[learner](),
            reporters.Csv(path),
        ])
    return simulation


simulation_builders = {
    'spotcheck': make_spotcheck_simulation,
    'snapshot': make_snapshot_simulation,
    'hammer': make_hammer_simulation,
    'standard': make_standard_simulation,
    'short_standard': make_short_standard_simulation,
    'mastery': make_mastery_simulation,
    'short_mastery': make_short_mastery_simulation,
}

def make_benchmark_simulation(study, baseline_name, configuration, learner):
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
    return simulation

def run_benchmark_simulations(study = None, configuration = None, learner = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    max_time = 2 * 60 * 60
    for baseline_name in baseline_names:
        simulation = make_benchmark_simulation(study, baseline_name, configuration, learner)
        runner = runners.LocalRunner(simulation, max_time)
        runner.run()
        if runners.RunQuery(simulation).was_escaped():
            break

def run_debug_benchmark_simulations(study = None, configuration = None, learner = None):
    study = study if study else get_study()
    baseline_names = baselines.get_baseline_names(study)
    for baseline_name in baseline_names:
        simulation = make_benchmark_simulation(study, baseline_name, configuration, learner)
        runner = runners.DebugRunner(simulation)
        runner.run()

if __name__ == '__main__':
    run_benchmark_simulations()
