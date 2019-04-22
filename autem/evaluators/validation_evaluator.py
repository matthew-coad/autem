from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import warnings
import time

class ValidationState:
    """
    Validation evaluation
    """

    def __init__(self):
        self.evaluated = False
        self.score = None

def get_validation_state(member):
    state = member.get_state("validation", lambda: ValidationState())
    return state

class ValidationEvaluator(Evaluater):
    """
    Validation evaluation component
    """

    def validate_member(self, member, required_league):

        validation_state = get_validation_state(member)
        if validation_state.evaluated:
            return None

        if member.league < required_league:
            return None

        scorer = member.get_scorer()
        loader = member.get_loader()
        pipeline = member.get_pipeline()

        x,y = loader.load_training_data(member)
        x_validation, y_validation = loader.load_validation_data(member)

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                pipeline.fit(x, y)
                y_pred = pipeline.predict(x_validation)
            except Exception as ex:
                member.fail(ex, "evaluate_member", "ValidationEvaluator")
                return None

        score = scorer.score(y_validation, y_pred)
        validation_state.score = score
        validation_state.evaluated = True

    def evaluate_member(self, member):
        super().evaluate_member(member)

        self.validate_member(member, member.get_specie().get_max_league())

    def rate_member(self, member):
        super().rate_member(member)

        self.validate_member(member, 1)

    def record_member(self, member, record):
        super().record_member(member, record)

        validation_state = get_validation_state(member)
        record.VE_score = validation_state.score
