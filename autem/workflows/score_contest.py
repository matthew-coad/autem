import numpy as np
from scipy import stats

from ..member_manager import MemberManager
from ..scorers import MemberScoreState

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class ScoreContest(MemberManager):
    """
    Determines fitness by comparing model scores 
    """

    def contest_members(self, contestant1, contestant2):

        specie = contestant1.get_specie()

        contestant1_scores = MemberScoreState.get(contestant1)
        contestant2_scores = MemberScoreState.get(contestant2)

        if contestant1_scores.score == contestant2_scores.score:
            return None

        if contestant1_scores.score > contestant2_scores.score:
            winner = contestant1
            loser = contestant2
        else:
            loser = contestant1
            winner = contestant2

        if loser.league <= winner.league:
            winner.victory()
            loser.defeat()
        else:
            winner.victory()
