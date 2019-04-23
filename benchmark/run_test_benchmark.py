if __name__ == '__main__':
    import context

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters

import benchmark.baselines as baselines
import benchmark.benchmarks as benchmark
import benchmark.utility as utility

import os
import openml

def get_test_study():
    return benchmark.get_study()

def get_test_baseline_name():
    return 'diabetes'

def get_test_simulations_path():
    return benchmark.get_simulations_path().joinpath("test")

def get_test_version():
    return benchmark.get_version()

def make_test_simulation(study, experiment, baseline_name, task_id, seed, path, memory, max_time = None):
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    version = get_test_version()
    simulation_name = "Test %s_%s_v%d" % (study, experiment, version)
    properties = {
        'study': study,
        'experiment': experiment,
        'dataset': dataset_name,
        'version': version
    }    
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(max_time=max_time),
            baselines.BaselineStats(baseline_name),
            hyper_learners.ClassificationSnapshot(),
            reporters.Csv(path),
        ], 
        seed = seed,
        n_jobs=6,
        identity = properties,
        memory=memory)
    return simulation

def run_test_simulation(baseline_name = None, seed = None):
    baseline_name = get_test_baseline_name() if baseline_name is None else baseline_name
    experiment = baseline_name if seed is None else "%s_%d" % (baseline_name, seed)
    study = get_test_study()
    seed = seed if not seed is None else 2
    version = get_test_version()

    configuration = baselines.get_baseline_configuration(baseline_name)
    path = get_test_simulations_path().joinpath(study).joinpath(experiment)
    memory = str(path.joinpath("cache"))

    utility.prepare_OpenML()
    task_id = configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "Test %s_%s_v%d" % (study, experiment, version)
    identity = {
        'study': study,
        'experiment': experiment,
        'dataset': dataset_name,
        'version': version
    }    
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.Snapshot(),
            baselines.BaselineStats(baseline_name),
            reporters.Csv(path),
            hyper_learners.ClassificationSnapshot(),
        ], 
        seed=seed,
        n_jobs=6,
        identity=identity,
        memory=memory)

    simulation = make_test_simulation(study, experiment, baseline_name, task_id, seed, path, memory = memory)
    simulation.run()

if __name__ == '__main__':
    run_test_simulation()
