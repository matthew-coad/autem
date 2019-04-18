from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation, get_score_evaluation
from .score_resources import ScoreResources, get_score_resources

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

    def contest_members(self, contestant1, contestant2):

        scorer = contestant1.get_specie().get_scorer()

        max_league = max(contestant1.league, contestant2.league)
        if max_league == 0:
            return None

        contestant1_score_evaluation = get_score_evaluation(contestant1)
        contestant1_score_resources = get_score_resources(contestant1)
        contestant2_score_evaluation = get_score_evaluation(contestant2)
        contestant2_score_resources = get_score_resources(contestant2)
        if not max_league in contestant1_score_resources.league_predictions or not max_league in contestant2_score_resources.league_predictions:
            return None

        contestant1_predictions = contestant1_score_resources.league_predictions[max_league]
        contestant2_predictions = contestant2_score_resources.league_predictions[max_league]
        inter_score = scorer.score(contestant1_predictions, contestant2_predictions)
        if inter_score < self.max_score:
            return None

        # The contestants make nearly identical predictions
        # kill one
        if contestant1.league < contestant2.league:
            contestant1.kill("Senior Identical")
        elif contestant1.league > contestant2.league:
            contestant2.kill("Senior Identical")
        elif contestant1.id < contestant2.id:
            contestant2.kill("Earlier Identical")
        elif contestant1.id > contestant2.id:
            contestant1.kill("Earlier Identical")
        else:
            raise RuntimeError("Unexpected condition")
            