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

    def contest_members(self, contestant1, contestant2, outcome):

        simulation = contestant1.simulation
        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        if outcome.is_conclusive():
            return None

        contestant1_score = contestant1.evaluation.score
        contestant2_score = contestant2.evaluation.score
        top_league = simulation.top_league

        if contestant1_score == contestant2_score and contestant1.id < contestant2.id:
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

        winner_scores = winner.evaluation.scores
        winner_std = winner.evaluation.score_std
        winner_score = winner.evaluation.score
        winner_duration = winner.evaluation.score_duration

        loser_score = loser.evaluation.score
        loser_duration = loser.evaluation.score_duration

        #if not winner_std is None and loser_duration > winner_duration * 3 and loser_score < winner_score - winner_std * 3:
        #    # The loser has an excessive run time and has a substantially poorer performance
        #    # Kill it outright as its unlikely to be a good solution and will substantially increase the runtime
        #    winner.evaluation.accuracy_contest = "Duration short"
        #    loser.evaluation.accuracy_contest = "Duration long"
        #    loser.fail("Duration long", "contest_members", "accuracy_contest")
        #    outcome.unconventional()
        #    return None

        if winner.league == 0 and loser.league > 0:
            winner.evaluation.accuracy_contest = "Upset Win"
            winner.promote()
            loser.evaluation.accuracy_contest = "Upset Loss"
            outcome.decisive(victor)
            return None

        winner.evaluation.accuracy_contest = "Win"
        loser.evaluation.accuracy_contest = "Loss"
        outcome.decisive(victor)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "accuracy_contest"):
            record.accuracy_contest = evaluation.accuracy_contest
        else:
            record.accuracy_contest = None
