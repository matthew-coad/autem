from ..simulators import Dataset, Role
from .rater import Rater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class HoldoutValidator(Rater):
    """
    Performs final validation by fitting the pipeline to the entire training data set
    and calculating the performance on the validation dataset
    """

    def __init__(self):
        """
        P value used to determine if the scores are significantly different
        """
        Rater.__init__(self, "CrossValidationRater")

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """

        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        x_validation, y_validation = loader.load_validation_data(simulation)

        pipeline = member.preparations.pipeline
        pipeline.fit(x, y)
        y_pred = pipeline.predict(x_validation)
        validation_rating = scorer.score(y_validation, y_pred)

        member.ratings.validation_rating = validation_rating

    def record_member(self, member, record):

        if hasattr(member.ratings, "validation_rating"):
            record.validation_rating = member.ratings.validation_rating
        else:
            record.validation_rating = None
