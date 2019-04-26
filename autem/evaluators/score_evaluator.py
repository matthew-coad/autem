from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, RepeatedKFold

import warnings
import time

class ScoreState:

    def __init__(self):
        self.quick_score = None
        self.quick_duration = None
        self.quick_predictions = None

        self.league_scores = {}
        self.league_durations = {}
        self.league_predictions = {}
        self.league_predictions = {}

        self.scores = []
        self.score = None
        self.score_std = None

        self.score_durations = []
        self.score_duration = None
        self.score_duration_std = None

class ScoreContainer:

    def get_score_state(self):
        return self.get_state("scores", lambda: ScoreState())

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
        max_league = specie.get_max_league()
        random_state = specie.get_random_state()

        data = specie.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        folds = RepeatedStratifiedKFold(n_splits=self.n_splits, n_repeats=max_league, random_state=random_state)
        i_leagues = [ (i_train, i_test) for i_train, i_test in folds.split(x, y) ]
        specie.set_state("i_leagues", i_leagues)

    def build_scores(self, member, repeat, start, stop):

        scorer = member.get_simulation().get_scorer()
        pipeline = member.get_pipeline()
        i_leagues = member.get_specie().get_state("i_leagues")

        data = member.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

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

        score_state = member.get_score_state()

        score_state.quick_score = quick_score
        score_state.quick_duration = quick_duration
        score_state.quick_predictions = predictions

        score_state.scores = [ quick_score ]
        score_state.score = quick_score
        score_state.score_std = None

        score_state.score_durations =  [ quick_duration ]
        score_state.score_duration = quick_duration
        score_state.score_duration_std = None

        return True

    def evaluate_league_1(self, member):
        """
        Evaluate league 1 score by finishing of the quick score
        """
        scores, durations, predictions = self.build_scores(member, 0, 1, self.n_splits)
        if scores is None:
            return False

        score_state = member.get_score_state()
        score_state.league_scores[1] = [ score_state.quick_score ] + scores
        score_state.league_durations[1] = [ score_state.quick_duration ] + durations
        quick_predictions = score_state.quick_predictions
        league_predictions = np.where(np.isnan(predictions), quick_predictions, predictions)
        score_state.league_predictions[1] = league_predictions
        return True

    def evaluate_league_scores(self, member, league):
        scores, durations, predictions = self.build_scores(member, 0, 0, self.n_splits)
        if scores is None:
            return False

        score_state = member.get_score_state()
        score_state.league_scores[league] = scores
        score_state.league_durations[league] = durations
        score_state.league_predictions[league] = predictions
        return True

    def evaluate_scores(self, member):
        score_state = member.get_score_state()
        scores = np.concatenate([ score_state.league_scores[l] for l in score_state.league_scores ])
        score_state.scores = scores.tolist()
        score_state.score = np.mean(scores)
        score_state.score_std = np.std(scores)

        durations = np.concatenate([ score_state.league_durations[l] for l in score_state.league_durations ])
        score_state.score_durations = durations.tolist()
        score_state.score_duration = np.mean(durations)
        score_state.score_duration_std = np.std(durations)

    def prepare_specie(self, specie):
        self.evaluate_folds(specie)

    def evaluate_member(self, member):
        super().evaluate_member(member)

        score_state = member.get_score_state()
        if member.league == 0 and score_state.quick_score is None:
            self.evaluate_quick_score(member)
            return None

        # At league level 1 add on the complete scores
        evaluated = False
        if member.league == 1 and not 1 in score_state.league_scores:
            evaluated = self.evaluate_league_1(member)

        # High league levels
        if member.league > 1 and not member.league in score_state.league_scores:
            evaluated = self.evaluate_league_scores(member, member.league)

        if evaluated:
            self.evaluate_scores(member)

    def record_member(self, member, record):
        super().record_member(member, record)

        score_state = member.get_score_state()
        record.SE_score = score_state.score
        record.SE_score_std = score_state.score_std
