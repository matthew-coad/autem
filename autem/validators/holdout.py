from ..simulation_manager import SimulationManager
from ..reporters import Reporter
from ..loaders import Dataset
from ..simulation_settings import SimulationSettings

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

class Holdout(SimulationManager, Reporter):
    """
    Validate a model using a heldout dataset
    """

    def __init__(self, validation_ratio = 0.2):
        self._validation_ratio = validation_ratio

    def get_validation_ratio(self):
        return self._validation_ratio

    def prepare_simulation(self, simulation):

        settings = SimulationSettings(simulation)
        random_state = settings.get_random_state()
        validation_ratio = self.get_validation_ratio()
        data = simulation.get_full_data()

        x_train, x_validation, y_train, y_validation = train_test_split(data.x, data.y, test_size=validation_ratio, random_state=random_state)
        train_data = Dataset(x_train, y_train, data.features)
        validation_data = Dataset(x_validation, y_validation, data.features)
        simulation.set_split_data(train_data, validation_data)

    def validate_member(self, member, required_league):

        validation_state = get_validation_state(member)
        if validation_state.evaluated:
            return None

        if member.league < required_league:
            return None

        simulation = member.get_simulation()
        scorer = simulation.get_scorer()

        training_data = simulation.get_training_data()
        validation_data = simulation.get_validation_data()
        pipeline = member.get_pipeline()

        x = training_data.x
        y = training_data.y
        x_validation = validation_data.x
        y_validation = validation_data.y

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
