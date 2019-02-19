from ..simulators import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class CrossValidationRater(Evaluater):
    """
    Evaluates a final model rating by using cross validation
    """

    def __init__(self, cv = 10):
        """
        P value used to determine if the scores are significantly different
        """
        Evaluater.__init__(self, "CrossValidationRater")
        self.cv = cv

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """

        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        pipeline = member.preparations.pipeline
        scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=self.cv)

        rating = scores.mean()
        rating_sd = scores.std()

        member.ratings.predictive_accuracy = rating
        member.ratings.predictive_accuracy_sd = rating_sd

        member.rated(rating, rating_sd)
