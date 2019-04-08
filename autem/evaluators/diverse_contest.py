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

    def get_score_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "score_evaluation"):
            evaluation.score_evaluation = ScoreEvaluation()
        return evaluation.score_evaluation

    def contest_members(self, contestant1, contestant2):

        contestant1.evaluation.inter_score = None
        contestant2.evaluation.inter_score = None
        contestant1.evaluation.diverse_contest = None
        contestant2.evaluation.diverse_contest = None

        simulation = contestant1.simulation
        scorer = simulation.resources.scorer
        max_league = max(contestant1.league, contestant2.league)
        contestant1_score_evaluation = self.get_score_evaluation(contestant1)
        contestant2_score_evaluation = self.get_score_evaluation(contestant2)

        if max_league == 0:
            return None

        if not max_league in contestant1_score_evaluation.league_predictions or not max_league in contestant2_score_evaluation.league_predictions:
            return None

        contestant1_predictions = contestant1_score_evaluation.league_predictions[max_league]
        contestant2_predictions = contestant2_score_evaluation.league_predictions[max_league]
        inter_score = scorer.score(contestant1_predictions, contestant2_predictions)
        contestant1.evaluation.inter_score = inter_score
        contestant2.evaluation.inter_score = inter_score
        if inter_score < self.max_score:
            return None

        # The contestants make identical predictions
        # kill one
        if contestant1_score_evaluation.score > contestant2_score_evaluation.score:
            contestant1.evaluation.diverse_contest = "Survive score"
            contestant2.evaluation.diverse_contest = "kill score"
            contestant2.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1_score_evaluation.score < contestant2_score_evaluation.score:
            contestant1.evaluation.diverse_contest = "kill score"
            contestant2.evaluation.diverse_contest = "Survive score"
            contestant1.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.league < contestant2.league:
            contestant1.evaluation.diverse_contest = "kill league"
            contestant2.evaluation.diverse_contest = "Survive league"
            contestant1.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.id < contestant2.id:
            contestant1.evaluation.diverse_contest = "Survive id"
            contestant2.evaluation.diverse_contest = "kill id"
            contestant2.fail("Identical", "contest_members", "DiverseContest")
        elif contestant1.id > contestant2.id:
            contestant1.evaluation.diverse_contest = "Kill id"
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
