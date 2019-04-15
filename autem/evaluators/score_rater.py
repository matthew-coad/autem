from .. import Dataset, Role
from .evaluator import Evaluater
from .score_evaluation import get_score_evaluation

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score
import warnings

class ScoreRater(Evaluater):
    """
    Uses the score to rate a model
    """

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """

        score_evaluation = get_score_evaluation(member)

        member.rated(score_evaluation.score, score_evaluation.score_std)
