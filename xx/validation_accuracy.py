from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

import warnings


class ValidationAccuracy(Evaluater):
    """
    Performs final validation by fitting the pipeline to the entire training data set
    and calculating the performance on the validation dataset
    """

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """

        scorer = member.get_scorer()
        loader = member.get_loader()
        pipeline = member.get_member_resources().pipeline

        x,y = loader.load_training_data(member)
        x_validation, y_validation = loader.load_validation_data(member)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                pipeline.fit(x, y)
                y_pred = pipeline.predict(x_validation)
            except Exception as ex:
                member.fail(ex, "rate_member", "ValidationAccuracy")
                return None

        validation_accuracy = scorer.score(y_validation, y_pred)
        member.ratings.validation_accuracy = validation_accuracy

    def record_member(self, member, record):

        if hasattr(member.ratings, "validation_accuracy"):
            record.validation_accuracy = member.ratings.validation_accuracy
        else:
            record.validation_accuracy = None
