if __name__ == '__main__':
    import context

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.validators as validators
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters

import benchmark.baselines as baselines
import benchmark.benchmarks as benchmark
import benchmark.utility as utility

import os
import openml

def run_balance_scale(seed):
    study = "DEV"
    baseline_name = "balance-scale"
    experiment = "svm_%s_s%d" % (baseline_name, seed)
    version = benchmark.get_version()
    simulation_name = "%s_%s_v%d" % (study, experiment, version)

    configuration = baselines.get_baseline_configuration(baseline_name)
    path = benchmark.get_simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    task_id = configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name

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
            hyper_learners.ClassificationSVM(),
            reporters.Csv(path),
        ], 
        seed=seed, n_jobs=4, identity=identity)
    simulation.run()

def run_balance_scale_baseline(seed):
    baseline_name = "balance-scale"
    experiment = "base_%s_s%d" % (baseline_name, seed)
    study = "DEV"
    version = benchmark.get_version()
    simulation_name = "%s_%s_v%d" % (study, experiment, version)

    configuration = baselines.get_baseline_configuration(baseline_name)
    path = benchmark.get_simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    task_id = configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name

    identity = {
        'study': study,
        'experiment': experiment,
        'dataset': dataset_name,
        'version': version
    }    
    
    simulation = autem.Simulation(simulation_name, seed,
        [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.SnapshotWorkflow(),
            baselines.BaselineStats(baseline_name),
            hyper_learners.ClassificationBaseline(),
            reporters.Csv(path),
        ])
    settings = autem.SimulationSettings(simulation)
    settings.set_identity(identity)
    settings.set_n_jobs(4)
    simulation.run()

if __name__ == '__main__':
    run_balance_scale_baseline(1)
