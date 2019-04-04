from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, RepeatedKFold

import warnings
import time

class ScoreEvaluator(Evaluater):
    """
    Component that evaluates scores for other components
    """

    def __init__(self):
        self.n_splits = 5

    def evaluate_folds(self, simulation):
        """
        Evaluate folds for the simulation
        """
        top_league = simulation.top_league
        random_state = simulation.random_state
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        folds = RepeatedStratifiedKFold(n_splits=self.n_splits, n_repeats=top_league, random_state=random_state)
        # folds = RepeatedKFold(n_splits=self.n_splits, n_repeats=top_league, random_state=random_state)
        i_leagues = [ (i_train, i_test) for i_train, i_test in folds.split(x, y) ]
        simulation.resources.i_leagues = i_leagues

    def prepare_scores(self, member):

        evaluation = member.evaluation
        if not hasattr(evaluation, "league_scores"):
            evaluation.quick_score = None
            evaluation.quick_duration = None
            evaluation.league_scores = {}
            evaluation.league_durations = {}
            evaluation.league_predictions = {}
            evaluation.scores = []
            evaluation.score = None
            evaluation.score_std = None

            evaluation.score_durations = []
            evaluation.score_duration = None
            evaluation.score_duration_std = None

    def build_scores(self, member, repeat, start, stop):

        evaluation = member.evaluation
        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader
        i_leagues = simulation.resources.i_leagues

        x,y = loader.load_training_data(simulation)
        scores = []
        durations = []
        predictions = np.empty(len(y))
        predictions[:] = np.nan
        for fold_index in range(start, stop):
            i_index = self.n_splits * repeat + fold_index
            i_train = i_leagues[i_index][0]
            i_test = i_leagues[i_index][1]
            x_train = x[i_train]
            y_train = y[i_train]
            x_test = x[i_test]
            y_test = y[i_test]
            start_time = time.time()

            pipeline = member.resources.pipeline
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                try:
                    pipeline.fit(x_train, y_train)
                    y_pred = pipeline.predict(x_test)
                except Exception as ex:
                    member.fail(ex, "score_evaluator", "ScoreEvaluator")
                    return (None, None, None)
            end_time = time.time()
            duration = end_time - start_time
            score = scorer.score(y_test, y_pred)
            scores.append(score)
            durations.append(duration)
            predictions[i_test] = y_pred
        return (scores, durations, predictions)

    def evaluate_quick_score(self, member):
        """
        Evaluate a quick score based on a single fit using the first entry in quick_fold
        """
        evaluation = member.evaluation
        evaluation.quick_score = None
        evaluation.quick_duration = None

        scores, durations, predictions = self.build_scores(member, 0, 0, 1)
        if scores is None:
            return False

        quick_score = scores[0]
        quick_duration = durations[0]

        evaluation.quick_score = quick_score
        evaluation.quick_duration = quick_duration
        evaluation.quick_predictions = predictions

        evaluation.scores = [ quick_score ]
        evaluation.score = quick_score
        evaluation.score_std = None

        evaluation.score_durations =  [ quick_duration ]
        evaluation.score_duration = quick_duration
        evaluation.score_duration_std = None

        return True

    def evaluate_league_1(self, member):
        """
        Evaluate league 1 score by finishing of the quick score
        """
        evaluation = member.evaluation

        scores, durations, predictions = self.build_scores(member, 0, 1, self.n_splits)
        if scores is None:
            return False

        evaluation.league_scores[1] = [ evaluation.quick_score ] + scores
        evaluation.league_durations[1] = [ evaluation.quick_duration ] + durations
        quick_predictions = evaluation.quick_predictions
        league_predictions = np.where(np.isnan(predictions), quick_predictions, predictions)
        evaluation.league_predictions[1] = league_predictions
        return True

    def evaluate_league_scores(self, member, league):
        evaluation = member.evaluation
        scores, durations, predictions = self.build_scores(member, 0, 0, self.n_splits)
        if scores is None:
            return False

        evaluation.league_scores[league] = scores
        evaluation.league_durations[league] = durations
        evaluation.league_predictions[league] = predictions
        return True

    def evaluate_scores(self, member):
        evaluation = member.evaluation

        scores = np.concatenate([ evaluation.league_scores[l] for l in evaluation.league_scores ])
        evaluation.scores = scores.tolist()
        evaluation.score = np.mean(scores)
        evaluation.score_std = np.std(scores)

        durations = np.concatenate([ evaluation.league_durations[l] for l in evaluation.league_durations ])
        evaluation.score_durations = durations.tolist()
        evaluation.score_duration = np.mean(durations)
        evaluation.score_duration_std = np.std(durations)

    def start_simulation(self, simulation):
        self.evaluate_folds(simulation)

    def evaluate_member(self, member):
        super().evaluate_member(member)

        self.prepare_scores(member)

        evaluation = member.evaluation
        if member.league == 0 and evaluation.quick_score is None:
            self.evaluate_quick_score(member)
            return None

        # At league level 1 add on the complete scores
        evaluated = False
        if member.league == 1 and not 1 in evaluation.league_scores:
            evaluated = self.evaluate_league_1(member)

        # High league levels
        if member.league > 1 and not member.league in evaluation.league_scores:
            evaluated = self.evaluate_league_scores(member, member.league)

        if evaluated:
            self.evaluate_scores(member)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "scores"):
            record.fits = len(evaluation.scores)
        else:
            record.fits = None

        if hasattr(evaluation, "score"):
            record.score = evaluation.score
        else:
            record.score = None

        if hasattr(evaluation, "score_std"):
            record.score_std = evaluation.score_std
        else:
            record.score_std = None

        if hasattr(evaluation, "score_duration"):
            record.score_duration = evaluation.score_duration
        else:
            record.score_duration = None
