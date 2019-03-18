from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class DiversityContest(Evaluater):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def evaluate_member(self, member):

        simulation = member.simulation
        resources = member.resources
        evaluation = member.evaluation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader
        random_state = simulation.random_state
        estimator = resources.pipeline

        top_league = simulation.top_league
        if member.league < top_league:
            return None

        if hasattr(evaluation, "predictions"):
            return None

        x,y = loader.load_training_data(simulation)

        start = time.time()

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                predictions = cross_val_predict(estimator, x, y, cv=5)
            except Exception as ex:
                member.fail(ex, "evaluate_predictions", "DiversityContest")
                return None

        end = time.time()
        duration = end - start

        evaluation.predictions = predictions
        evaluation.prediction_duration = duration

    def contest_members(self, contestant1, contestant2, outcome):

        contestant1.evaluation.diversity_contest = None
        contestant2.evaluation.diversity_contest = None

        simulation = contestant1.simulation
        scorer = simulation.resources.scorer

        top_league = simulation.top_league
        if not hasattr(contestant1.evaluation, "predictions") or not hasattr(contestant2.evaluation, "predictions"):
            return None

        other_members = [ m for m in simulation.members if m.league == top_league and m.id != contestant1.id and m.id != contestant2.id and hasattr(m.evaluation, "predictions") ]
        if not other_members:
            return None

        contest1_scores = [ scorer.score(m.evaluation.predictions, contestant1.evaluation.predictions) for m in other_members ]
        contest1_score = np.mean(contest1_scores)

        contest2_scores = [ scorer.score(m.evaluation.predictions, contestant2.evaluation.predictions) for m in other_members ]
        contest2_score = np.mean(contest2_scores)

        if contest1_score < contest2_score:
            contestant1.evaluation.diversity_contest = "Win"
            contestant2.evaluation.diversity_contest = "Loss"
            contestant1.victory()
            contestant2.defeat()

        if contest1_score > contest2_score:
            contestant1.evaluation.diversity_contest = "Loss"
            contestant2.evaluation.diversity_contest = "Win"
            contestant1.defeat()
            contestant2.victory()

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "diversity_contest"):
            record.diversity_contest = evaluation.diversity_contest
        else:
            record.diversity_contest = None


