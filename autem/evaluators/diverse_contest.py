from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

class DiverseContest(Evaluater):
    """
    Verify that there is notable difference between contesting members
    """

    def __init__(self, max_score):
        """
        Max accuracy 
        
        """
        self.max_score = max_score

    def evaluate_member(self, member):
        """
        Evaluate the cross validated predictions for the given member
        """
        simulation = member.simulation
        resources = member.resources
        evaluation = member.evaluation
        loader = simulation.resources.loader
        estimator = resources.pipeline

        if hasattr(evaluation, "predictions"):
            return None

        x,y = loader.load_training_data(simulation)

        start = time.time()

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                predictions = cross_val_predict(estimator, x, y, cv=5)
            except Exception as ex:
                member.fail(ex, "evaluate_predictions", "DiverseContest")
                return None

        end = time.time()
        duration = end - start

        evaluation.predictions = predictions
        evaluation.prediction_duration = duration

    def contest_members(self, contestant1, contestant2, outcome):

        contestant1.evaluation.inter_score = None
        contestant2.evaluation.inter_score = None
        contestant1.evaluation.diverse_contest = None
        contestant2.evaluation.diverse_contest = None

        simulation = contestant1.simulation
        scorer = simulation.resources.scorer
        max_league = max(contestant1.league, contestant2.league)

        if max_league == 0:
            return None

        inter_score = scorer.score(contestant1.evaluation.predictions, contestant2.evaluation.predictions)
        contestant1.evaluation.inter_score = inter_score
        contestant2.evaluation.inter_score = inter_score
        if inter_score < self.max_score:
            return None

        # The contestants make identical predictions
        # Eliminate one
        if contestant1.evaluation.score > contestant2.evaluation.score:
            contestant1.evaluation.diverse_contest = "Survive score"
            contestant2.evaluation.diverse_contest = "Eliminate score"
            contestant2.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.evaluation.score < contestant2.evaluation.score:
            contestant1.evaluation.diverse_contest = "Eliminate score"
            contestant2.evaluation.diverse_contest = "Survive score"
            contestant1.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.league < contestant2.league:
            contestant1.evaluation.diverse_contest = "Eliminate league"
            contestant2.evaluation.diverse_contest = "Survive league"
            contestant1.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.id < contestant2.id:
            contestant1.evaluation.diverse_contest = "Survive id"
            contestant2.evaluation.diverse_contest = "Eliminate id"
            contestant2.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.id > contestant2.id:
            contestant1.evaluation.diverse_contest = "Eliminate id"
            contestant2.evaluation.diverse_contest = "Survive id"
            contestant1.fail("Identical", "contest_members", "DiverseContest")
        else:
            raise RuntimeError("Unexpected condition")

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "diverse_contest"):
            record.inter_score = evaluation.inter_score
            record.diverse_contest = evaluation.diverse_contest
        else:
            record.inter_score = None
            record.diverse_contest = None
