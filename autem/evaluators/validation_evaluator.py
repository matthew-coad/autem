from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

from .validation_evaluation import ValidationEvaluation

import warnings
import time

class ValidationEvaluator(Evaluater):
    """
    Validation evaluation component
    """

    def evaluate_member(self, member):
        super().evaluate_member(member)

        simulation = member.simulation
        evaluation = member.evaluation
        if hasattr(evaluation, "validation_evaluation"):
            return None

        if member.league < simulation.top_league:
            return None

        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        x_validation, y_validation = loader.load_validation_data(simulation)

        pipeline = member.resources.pipeline
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                pipeline.fit(x, y)
                y_pred = pipeline.predict(x_validation)
            except Exception as ex:
                member.fail(ex, "evaluate_member", "ValidationEvaluator")
                return None

        score = scorer.score(y_validation, y_pred)

        validation_evaluation = ValidationEvaluation(score)
        evaluation.validation_evaluation = validation_evaluation

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        validation_evaluation = evaluation.validation_evaluation if hasattr(evaluation, "validation_evaluation") else None
        if validation_evaluation:
            record.VE_score = validation_evaluation.score
        else:
            record.VE_score = None

