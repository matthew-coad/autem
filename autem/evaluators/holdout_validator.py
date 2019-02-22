from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class HoldoutValidator(Evaluater):
    """
    Performs final validation by fitting the pipeline to the entire training data set
    and calculating the performance on the validation dataset
    """

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

        pipeline = member.resources.pipeline
        pipeline.fit(x, y)
        y_pred = pipeline.predict(x_validation)
        validation_accuracy = scorer.score(y_validation, y_pred)

        member.ratings.validation_accuracy = validation_accuracy

    def record_member(self, member, record):

        if hasattr(member.ratings, "validation_accuracy"):
            record.validation_accuracy = member.ratings.validation_accuracy
        else:
            record.validation_accuracy = None
