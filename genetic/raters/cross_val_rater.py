from ..simulators import Dataset, Role
from .rater import Rater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class CrossValidationRater(Rater):
    """
    Evaluates a final model rating by using cross validation
    """

    def __init__(self, cv = 10):
        """
        P value used to determine if the scores are significantly different
        """
        Rater.__init__(self, "CrossValidationRater")
        self.cv = cv

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """

        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_divided(member)
        pipeline = member.preparations.pipeline
        scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=self.cv)

        rating = scores.mean()
        member.rated(rating)
