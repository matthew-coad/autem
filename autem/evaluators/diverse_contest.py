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

        if not max_league in contestant1.evaluation.league_predictions or not max_league in contestant2.evaluation.league_predictions:
            return None

        contestant1_predictions = contestant1.evaluation.league_predictions[max_league]
        contestant2_predictions = contestant2.evaluation.league_predictions[max_league]
        inter_score = scorer.score(contestant1_predictions, contestant2_predictions)
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