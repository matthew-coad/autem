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

import hyper.configuration as configuration
import config
import openml
import os

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')

def make_snapshot_simulation(baseline_name):
    prepare_OpenML()

    study = "snapshot"
    hyper_configuration = configuration.get_hyper_configuration(baseline_name)
    task_id = hyper_configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    name = "%s %s" % (baseline_name,study)
    path = configuration.get_hyper_simulations_path().joinpath(study).joinpath(baseline_name)
    n_jobs = 4
    seed = 1
    memory = str(path.joinpath("cache"))

    identity = {
        'study': study,
        'dataset': baseline_name,
        'scorer': 'League1x10',
        'workflow': 'snapshot',
        'learner': 'baseline',
    }    

    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.SnapshotWorkflow(),
            hyper_learners.ClassificationBaseline(),
            reporters.Csv(path),
        ])

    settings = autem.SimulationSettings(simulation)
    settings.set_identity(identity)
    settings.set_n_jobs(4)
    settings.set_seed(seed)
    settings.set_memory(memory)

    return simulation

learner_builders = {
    'linear': hyper_learners.ClassificationLinear,
    'trees': hyper_learners.ClassificationTrees,
    'svm': hyper_learners.ClassificationSVM,
    'bayes': hyper_learners.ClassificationBayes,
}

def make_standard_simulation(study, baseline_name, hyperlearner):
    prepare_OpenML()

    hyper_configuration = configuration.get_hyper_configuration(baseline_name)
    task_id = hyper_configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    name = "%s %s" % (baseline_name, study)
    path = configuration.get_hyper_simulations_path().joinpath(study).joinpath(baseline_name)
    n_jobs = 4
    seed = 1
    memory = str(path.joinpath("cache"))

    identity = {
        'study': study,
        'dataset': baseline_name,
        'scorer': 'League1x10',
        'workflow': 'standard',
        'learner': hyperlearner,
    }    

    simulation = autem.Simulation(
        name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.LeagueScorer(scorers.accuracy_score, [ [ 1, 4, 5 ] ]),
            workflows.StandardWorkflow(),
            learner_builders[hyperlearner](),
            reporters.Csv(path),
        ])

    settings = autem.SimulationSettings(simulation)
    settings.set_identity(identity)
    settings.set_n_jobs(4)
    settings.set_seed(seed)
    settings.set_memory(memory)

    return simulation

def run_snapshot_analysis(debug):
    baseline_names = configuration.get_hyper_names()
    max_time = 1 * 60 * 60
    for baseline_name in baseline_names:
        simulation = make_snapshot_simulation(baseline_name)
        runner = runners.LocalRunner(simulation, max_time) if not debug else runners.DebugRunner(simulation)
        runner.run()
        if runners.RunQuery(simulation).was_escaped():
            break

def run_standard_analysis(study, hyperlearner, debug):
    hyper_analysis = 
    baseline_names = configuration.get_hyper_names()
    max_time = 2 * 60 * 60
    for baseline_name in baseline_names:
        simulation = make_standard_simulation(study, baseline_name, hyperlearner)
        runner = runners.LocalRunner(simulation, max_time) if not debug else runners.DebugRunner(simulation)
        runner.run()
        if runners.RunQuery(simulation).was_escaped():
            break

if __name__ == '__main__':
    run_standard_analysis("linear", "linear", False)
    run_standard_analysis("bayes", "bayes", False)

