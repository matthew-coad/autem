from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score
import warnings

class CrossValidationRater(Evaluater):
    """
    Evaluates a final model rating by using cross validation
    """

    def __init__(self, cv = 10):
        """
        P value used to determine if the scores are significantly different
        """
        self.cv = cv

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """
        raise NotImplementedError()

        scorer = member.get_simulation().get_scorer()

        data = member.get_simulation().get_training_data()
        x = data.x
        y = data.y
        pipeline = member.get_pipeline()

        try:
            scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=self.cv, error_score='raise')
        except Exception as ex:
            member.fail(ex, "rate_member", "CrossValidationRater")
            return None

        rating = scores.mean()
        rating_sd = scores.std()

        member.rated(rating, rating_sd)
