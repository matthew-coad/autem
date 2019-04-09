# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.preprocessors as preprocessors
import autem.learners.classification as learners
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
    return "SS"

def get_simulations_path():
    return Path("benchmark/simulations")

def get_version():
    return 13

def make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path, properties = {}):
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

            #evaluators.ChoiceEvaluator(),
            makers.RandomMaker(),
            #makers.TopChoiceMaker(),
            makers.CrossoverMaker(),

            evaluators.ScoreEvaluator(),
            evaluators.DurationEvaluator(),
            evaluators.ValidationEvaluator(),

            evaluators.ScoreContest(),
            evaluators.StabilityContest(),
            # evaluators.DiverseContest(0.99),
            # evaluators.VotingContest(),
            
            evaluators.SurvivalJudge(),
            evaluators.PromotionJudge(),

            evaluators.CrossValidationRater(),
            baselines.BaselineStats(baseline_name),

            reporters.Path(path),

            # Scalers
            autem.Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.Binarizer(),
                preprocessors.BoxCoxTransform(),
                preprocessors.YeoJohnsonTransform()
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
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
            ]),

            # Approximators
            autem.Choice("Approximator", [
                preprocessors.NoApproximator(),
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ]),

            autem.Choice("Learner", [
                learners.GaussianNB(),
                learners.BernoulliNB(),
                learners.MultinomialNB(),
                learners.DecisionTreeClassifier(),
                learners.KNeighborsClassifier(),
                learners.LinearSVC(),
                learners.RadialBasisSVC(),
                learners.PolySVC(),
                learners.LogisticRegression(),
                learners.LinearDiscriminantAnalysis(),

                learners.RandomForestClassifier(),
                learners.ExtraTreesClassifier(),
            ]),
        ], 
        population_size = population_size,
        seed = seed,
        properties = properties,
        n_jobs=6)
    return simulation

def run_benchmark_simulation(study, baseline_name):
    experiment = baseline_name
    baseline_configuration = baselines.get_baseline_configuration(baseline_name)
    task_id = baseline_configuration["task_id"]
    seed = 1
    epochs = 25
    rounds = 20
    max_time = 2 * 60 * 60
    population_size = 20
    path = get_simulations_path().joinpath(study).joinpath(experiment)

    utility.prepare_OpenML()
    simulation = make_openml_light_classifier_simulation(study, experiment, baseline_name, task_id, seed, population_size, path)
    simulation.run_simulation(rounds, epochs, max_time)
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
