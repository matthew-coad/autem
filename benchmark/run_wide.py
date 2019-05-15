if __name__ == '__main__':
    import context

import autem
import autem.scorers as scorers
import autem.workflows as workflows
import autem.validators as validators
import autem.hyper_learners as hyper_learners
import autem.loaders as loaders
import autem.reporters as reporters

import autem.learners.classification as learners
import autem.preprocessors as preprocessors

import benchmark.baselines as baselines
import benchmark.benchmarks as benchmark
import benchmark.utility as utility

import os
import openml

from pathlib import Path

def get_simulations_path():
    return Path("benchmark/simulations/test")

def get_version():
    return 15

def run_wide_custom(baseline_name):

    seed = 1
    study = "WD1"
    experiment = "KNN1"
    version = benchmark.get_version()
    simulation_name = "%s_%s" % (study, experiment)

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

    name = "'%s_%s v%d'" % (study, experiment, version)
    identity = {
        'study': study,
        'experiment': experiment,
        'dataset': baseline_name,
        'version': version,
        'configuration': configuration,
    }    

    max_time = 2 * 60 * 60
    n_jobs = 4
    seed = 1
    path = get_simulations_path().joinpath(study).joinpath(experiment)
    memory = str(path.joinpath("cache"))

    utility.prepare_OpenML()
    hyper_learner = [

        # Scalers
        autem.Choice("Scaler", [
            #preprocessors.RobustScaler(),
            preprocessors.StandardScaler(),
            #preprocessors.BoxCoxTransform(),
            #preprocessors.YeoJohnsonTransform()
        ]),


        # Feature Selectors
        autem.Choice("Selector", [
            preprocessors.NoSelector(),
            preprocessors.SelectPercentile(),
            preprocessors.VarianceThreshold()
        ]),

        # Feature Reducers
        autem.Choice("Reducer", [
            preprocessors.NoReducer(),
            #preprocessors.FastICA(),
            #preprocessors.FeatureAgglomeration(),
            preprocessors.PCA(),
        ]),

        # Approximators
        autem.Choice("Approximator", [
            preprocessors.NoApproximator(),
        ]),

        autem.Choice("Learner", [
            #learners.GaussianNB(),
            #learners.BernoulliNB(),
            #learners.MultinomialNB(),
            #learners.DecisionTreeClassifier(),
            learners.KNeighborsClassifier(),
            #learners.LinearSVC(),
            #learners.LogisticRegression(),
            #learners.LinearDiscriminantAnalysis(),
        ]),
    ]

    components = [
            loaders.OpenMLLoader(data_id),
            scorers.Accuracy(),
            workflows.MasteryWorkflow(),
            baselines.BaselineStats(identity['dataset']),
            reporters.Csv(path),
    ] + hyper_learner

    simulation = autem.Simulation(name, components)

    settings = autem.SimulationSettings(simulation)
    settings.set_identity(identity)
    settings.set_n_jobs(n_jobs)
    settings.set_seed(seed)
    settings.set_memory(memory)
    settings.set_max_time(max_time)

    simulation.run()

if __name__ == '__main__':
    run_wide_custom("har")
