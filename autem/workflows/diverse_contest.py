from ..member_manager import MemberManager
from ..scorers import MemberScoreState
from ..scorers import ScoreQuery

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

class DiverseContest(MemberManager):
    """
    Verify that there is notable difference between contesting members
    """

    def __init__(self, max_score):
        """
        Max accuracy 
        
        """
        self.max_score = max_score

    def contest_members(self, contestant1, contestant2):

        scorer = ScoreQuery(contestant1.get_simulation()).get_metric()

        max_league = max(contestant1.league, contestant2.league)
        if max_league == 0:
            return None

        contestant1_score_state = MemberScoreState.get(contestant1)
        contestant2_score_state = MemberScoreState.get(contestant2)
        if not max_league in contestant1_score_state.league_predictions or not max_league in contestant2_score_state.league_predictions:
            return None

        contestant1_predictions = contestant1_score_state.league_predictions[max_league]
        contestant2_predictions = contestant2_score_state.league_predictions[max_league]
        inter_score = scorer(contestant1_predictions, contestant2_predictions)
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
            