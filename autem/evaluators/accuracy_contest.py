from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time
import warnings

class AccuracyContest(Evaluater):
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
        super().evaluate_member(member)

        evaluation = member.evaluation

        if not hasattr(evaluation, "scores"):
            member.evaluation.scores = {}
            member.evaluation.durations = []

        if member.league in evaluation.scores:
            return None

        simulation = member.simulation
        resources = member.resources
        random_state = simulation.random_state
        n_jobs = simulation.n_jobs

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)

        start = time.time()
        pipeline = resources.pipeline
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=5, error_score='raise')
            except Warning as ex:
                raise ex
        evaluation.scores[member.league] = scores
        league_scores = [ evaluation.scores[league] for league in evaluation.scores ]
        evaluation.score = np.concatenate(league_scores).mean()

        end = time.time()
        duration = end - start

        evaluation.durations.append(duration)
        evaluation.duration = duration

    def contest_members(self, contestant1, contestant2, outcome):

        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        if outcome.is_conclusive():
            return None

        contestant1_score = contestant1.evaluation.score
        contestant2_score = contestant2.evaluation.score

        if contestant1_score == contestant2_score:
            contestant1.evaluation.accuracy_contest = "Inconclusive"
            contestant2.evaluation.accuracy_contest = "Inconclusive"
            outcome.inconclusive()
            return None

        if contestant1_score > contestant2_score:
            victor = 1
        else:
            victor = 2

        winner = contestant1 if victor == 1 else contestant2
        loser = contestant2 if victor == 1 else contestant1
        winner.evaluation.accuracy_contest = "Win"
        loser.evaluation.accuracy_contest = "Loss"
        outcome.decisive(victor)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "score"):
            record.accuracy = evaluation.score
        else:
            record.accuracy = None

        evaluation = member.evaluation
        if hasattr(evaluation, "duration"):
            record.duration = evaluation.duration
        else:
            record.duration = None

        if hasattr(evaluation, "accuracy_contest"):
            record.accuracy_contest = evaluation.accuracy_contest
        else:
            record.accuracy_contest = None
