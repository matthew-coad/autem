if __name__ == '__main__':
    import context

# Must import Autem before *anything* except context to set up the warning interceptors

import autem
import autem.scorers as scorers
import autem.preprocessors as preprocessors
import autem.learners.regression as learners
import autem.loaders as loaders
import autem.reporters as reporters
import autem.evaluators as evaluators
import autem.makers as makers

import time
import datetime
from pathlib import Path

from pandas import read_csv    

def get_models_path():
    return Path("autem/models")

def get_pace_version():
    return 11

# Load pace dataset
def load_pace_df():
    filename = get_models_path().joinpath('data').joinpath('pace.csv')
    df = read_csv(filename)
    y = df['final_standard_score'].to_numpy()
    numeric_x = df[['epoch', 'standard_score', 'duration']].to_numpy()
    return (y, numeric_x)

def make_pace_simulation(study, seed, population_size, path, properties = {}):

    data_name = 'pace'
    y,numeric_x = load_pace_df()
    version = get_pace_version()
    simulation_name = "%s_v%d" % (study, version)
    properties['study'] = study
    properties['version'] = version
    
    simulation = autem.Simulation(
        simulation_name,
        [
            loaders.Data(data_name, y, numeric_x),
            scorers.NegativeRMSE(),

            makers.RandomMaker(),

            evaluators.ScoreEvaluator(),
            evaluators.AccuracyContest(),
            evaluators.DiverseContest(0.99),
            evaluators.VotingContest(),
            evaluators.SurvivalJudge(),
            evaluators.PromotionJudge(),

            evaluators.CrossValidationRater(),
            evaluators.ValidationAccuracy(),

            reporters.Path(path),

            # Approximators
            autem.Choice("Approximator", [
                preprocessors.NoApproximator(),
                preprocessors.RBFSampler(),
                preprocessors.Nystroem(),
            ]),

            autem.Choice("Learner", [
                learners.ElasticNetCV(), 
                learners.LinearRegression(), 
                learners.LassoLarsCV(), 
                learners.LinearSVR(), 
                learners.RidgeCV()
            ]),
        ], 
        population_size = population_size,
        seed = seed,
        properties = properties,
        n_jobs=6)
    return simulation

def simulation_finished(simulation, start_time, epochs, max_time):
    duration = time.time() - start_time
    return not simulation.running or simulation.epoch == epochs or (max_time is not None and duration >= max_time)

def run_simulation(simulation, steps, epochs, max_time = None):
    print("-----------------------------------------------------")
    start_time = time.time()
    today = datetime.datetime.now()
    print("Running %s - Started %s" % (simulation.name, today.strftime("%x %X")))
    simulation.start()

    finished = False
    while not finished:
        simulation.run(steps)
        finished = simulation_finished(simulation, start_time, epochs, max_time)
        if finished:
            simulation.finish()
        simulation.report()
    duration = time.time() - start_time
    print("%s finished - Duration %s" % (simulation.name, duration))

def run_pace_simulation(study):
    seed = 1
    epochs = 5
    steps = 200
    max_time = 60 * 60
    population_size = 20
    path = get_models_path().joinpath("simulations").joinpath(study)

    simulation = make_pace_simulation(study, seed, population_size, path)
    run_simulation(simulation, steps, epochs, max_time)
    autem.ReportManager(path).update_combined_reports()

if __name__ == '__main__':
    run_pace_simulation("distance")
