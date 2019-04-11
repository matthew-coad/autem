from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyClassifier

class DummyClassifierAccuracy(Evaluater):
    """
    Evaluates a final dummy classification by using the dummy classifer
    """

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """

        simulation = member.simulation
        random_state = simulation.random_state
        scorer = simulation.get_scorer()
        loader = simulation.get_loader()

        x,y = loader.load_training_data(simulation)

        learner = DummyClassifier(random_state = random_state)
        learner.fit(x, y)
        y_pred = learner.predict(x)

        accuracy = scorer.score(y, y_pred)
        member.ratings.dummy_accuracy = accuracy

    def record_member(self, member, record):
        if hasattr(member.ratings, "dummy_accuracy"):
            record.dummy_accuracy = member.ratings.dummy_accuracy
        else:
            record.dummy_accuracy = None

