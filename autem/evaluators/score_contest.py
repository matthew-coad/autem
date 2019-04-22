from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class ScoreContest(Evaluater):
    """
    Determines fitness by comparing model scores 
    """

    def contest_members(self, contestant1, contestant2):

        specie = contestant1.get_specie()

        contestant1_score = contestant1.get_score_state().score
        contestant2_score = contestant2.get_score_state().score

        if contestant1_score == contestant2_score:
            return None

        if contestant1_score > contestant2_score:
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
