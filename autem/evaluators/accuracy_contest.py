from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

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

    def evaluate_league_scores(self, member, league):

        simulation = member.simulation
        resources = member.resources
        evaluation = member.evaluation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader
        random_state = simulation.random_state

        x,y = loader.load_training_data(simulation)

        start = time.time()
        pipeline = resources.pipeline

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                league_scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=5, error_score='raise')
            except Exception as ex:
                member.fail(ex, "evaluate_league_scores", "AccuracyContest")
                return None

        evaluation.league_scores[member.league] = league_scores
        scores = np.concatenate([ evaluation.league_scores[l] for l in evaluation.league_scores ])
        evaluation.scores = scores.tolist()

        evaluation.score = np.mean(scores)
        evaluation.score_std = scores.std()

        end = time.time()
        duration = end - start
        evaluation.durations.append(duration)
        evaluation.duration = np.mean(evaluation.durations)
        evaluation.duration_std = np.std(evaluation.durations)

    def evaluate_member(self, member):
        super().evaluate_member(member)

        evaluation = member.evaluation

        if not hasattr(evaluation, "league_scores"):
            evaluation.league_scores = {}
            evaluation.scores = []
            evaluation.score = None
            evaluation.score_std = None

            evaluation.durations = []
            evaluation.duration = None
            evaluation.duration_std = None

        if member.league in evaluation.league_scores:
            return None

        self.evaluate_league_scores(member, member.league)

    def contest_members(self, contestant1, contestant2, outcome):

        simulation = contestant1.simulation
        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        if outcome.is_conclusive():
            return None

        contestant1_score = contestant1.evaluation.score
        contestant2_score = contestant2.evaluation.score
        top_league = simulation.top_league

        if contestant1_score == contestant2_score and contestant1.league == contestant2.league and contestant1.league == top_league:
            # Accuracies are identical
            # Simulation can get stuck here
            # Kill one member at random
            contestant1.fail("Top score identical", "evaluate", "accuracy_contest")
            contestant1.evaluation.accuracy_contest = "Top score identical"
            contestant1.evaluation.accuracy_contest = "Top score identical"
            outcome.unconventional()
            return None
        elif contestant1_score == contestant2_score and contestant1.league < contestant2.league:
            victor = 1
        elif contestant1_score == contestant2_score and contestant2.league < contestant2.league:
            victor = 2
        elif contestant1_score == contestant2_score and contestant1.id < contestant2.id:
            victor = 1
        elif contestant1_score == contestant2_score and contestant1.id > contestant2.id:
            victor = 2
        elif contestant1_score > contestant2_score:
            victor = 1
        elif contestant1_score < contestant2_score:
            victor = 2
        else:
            raise RuntimeError("Victory condition not found")

        winner = contestant1 if victor == 1 else contestant2
        loser = contestant2 if victor == 1 else contestant1

        # If the losers score is within one standard deviation of the winners score
        # but it has a shorter run-time then have it win instead

        winner_scores = winner.evaluation.scores
        winner_std = winner.evaluation.score_std
        winner_score = winner.evaluation.score
        winner_duration = winner.evaluation.duration

        loser_score = loser.evaluation.score
        loser_duration = loser.evaluation.duration

        if loser_duration > winner_duration * 3 and loser_score < winner_score - winner_std * 3:
            # The loser has an excessive run time and has a substantially poorer performance
            # Kill it outright as its unlikely to be a good solution and will substantially increase the runtime
            winner.evaluation.accuracy_contest = "Duration short"
            loser.evaluation.accuracy_contest = "Duration long"
            loser.fail("Duration long", "contest_members", "accuracy_contest")
            outcome.unconventional()
            return None

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

        if hasattr(evaluation, "score_std"):
            record.score_std = evaluation.score_std
        else:
            record.score_std = None

        evaluation = member.evaluation
        if hasattr(evaluation, "duration"):
            record.duration = evaluation.duration
        else:
            record.duration = None

        if hasattr(evaluation, "accuracy_contest"):
            record.accuracy_contest = evaluation.accuracy_contest
        else:
            record.accuracy_contest = None
