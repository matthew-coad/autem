from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation, get_score_evaluation
from .score_resources import ScoreResources, get_score_resources

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

    def evaluate_folds(self, specie):
        """
        Evaluate folds for the specie
        """
        max_league = specie.get_settings().get_max_league()
        random_state = specie.get_random_state()
        loader = specie.get_loader()

        x,y = loader.load_training_data(specie.get_simulation())
        folds = RepeatedStratifiedKFold(n_splits=self.n_splits, n_repeats=max_league, random_state=random_state)
        i_leagues = [ (i_train, i_test) for i_train, i_test in folds.split(x, y) ]
        specie.set_state("i_leagues", i_leagues)

    def build_scores(self, member, repeat, start, stop):

        specie = member.get_specie()
        scorer = specie.get_scorer()
        loader = specie.get_loader()
        i_leagues = specie.get_state("i_leagues")
        pipeline = member.get_resources().pipeline

        x,y = loader.load_training_data(member.get_specie().get_simulation())
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
        scores, durations, predictions = self.build_scores(member, 0, 0, 1)
        if scores is None:
            return False

        quick_score = scores[0]
        quick_duration = durations[0]

        score_evaluation = get_score_evaluation(member)
        score_resources = get_score_resources(member)

        score_evaluation.quick_score = quick_score
        score_evaluation.quick_duration = quick_duration
        score_resources.quick_predictions = predictions

        score_evaluation.scores = [ quick_score ]
        score_evaluation.score = quick_score
        score_evaluation.score_std = None

        score_evaluation.score_durations =  [ quick_duration ]
        score_evaluation.score_duration = quick_duration
        score_evaluation.score_duration_std = None

        return True

    def evaluate_league_1(self, member):
        """
        Evaluate league 1 score by finishing of the quick score
        """
        scores, durations, predictions = self.build_scores(member, 0, 1, self.n_splits)
        if scores is None:
            return False

        score_evaluation = get_score_evaluation(member)
        score_resources = get_score_resources(member)
        score_evaluation.league_scores[1] = [ score_evaluation.quick_score ] + scores
        score_evaluation.league_durations[1] = [ score_evaluation.quick_duration ] + durations
        quick_predictions = score_resources.quick_predictions
        league_predictions = np.where(np.isnan(predictions), quick_predictions, predictions)
        score_resources.league_predictions[1] = league_predictions
        return True

    def evaluate_league_scores(self, member, league):
        scores, durations, predictions = self.build_scores(member, 0, 0, self.n_splits)
        if scores is None:
            return False

        score_evaluation = get_score_evaluation(member)
        score_resources = get_score_resources(member)
        score_evaluation.league_scores[league] = scores
        score_evaluation.league_durations[league] = durations
        score_resources.league_predictions[league] = predictions
        return True

    def evaluate_scores(self, member):
        score_evaluation = get_score_evaluation(member)

        scores = np.concatenate([ score_evaluation.league_scores[l] for l in score_evaluation.league_scores ])
        score_evaluation.scores = scores.tolist()
        score_evaluation.score = np.mean(scores)
        score_evaluation.score_std = np.std(scores)

        durations = np.concatenate([ score_evaluation.league_durations[l] for l in score_evaluation.league_durations ])
        score_evaluation.score_durations = durations.tolist()
        score_evaluation.score_duration = np.mean(durations)
        score_evaluation.score_duration_std = np.std(durations)

    def start_specie(self, specie):
        self.evaluate_folds(specie)

    def evaluate_member(self, member):
        super().evaluate_member(member)

        score_evaluation = get_score_evaluation(member)
        if member.league == 0 and score_evaluation.quick_score is None:
            self.evaluate_quick_score(member)
            return None

        # At league level 1 add on the complete scores
        evaluated = False
        if member.league == 1 and not 1 in score_evaluation.league_scores:
            evaluated = self.evaluate_league_1(member)

        # High league levels
        if member.league > 1 and not member.league in score_evaluation.league_scores:
            evaluated = self.evaluate_league_scores(member, member.league)

        if evaluated:
            self.evaluate_scores(member)

    def record_member(self, member, record):
        super().record_member(member, record)

        score_evaluation = get_score_evaluation(member)
        record.SE_score = score_evaluation.score
        record.SE_score_std = score_evaluation.score_std
