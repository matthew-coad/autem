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

def run_balance_scale():
    baseline_name = "balance-scale"
    experiment = baseline_name
    study = "DEV"
    seed = 1
    version = benchmark.get_version()

    configuration = baselines.get_baseline_configuration(baseline_name)
    path = benchmark.get_simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    task_id = configuration["task_id"]
    task = openml.tasks.get_task(task_id)
    data_id = task.dataset_id
    dataset = openml.datasets.get_dataset(data_id)
    dataset_name = dataset.name
    simulation_name = "%s_%s_v%d" % (study, experiment, version)

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
            workflows.Standard(),
            baselines.BaselineStats(baseline_name),

            hyper_learners.ClassificationSnapshot(),
            reporters.Csv(path),
        ], 
        seed=seed, n_jobs=4, identity=identity)
    simulation.run()

if __name__ == '__main__':
    run_balance_scale()
