from ..simulators import Parameter, Component, Dataset, Role

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats

import time

class Learner(Component):

    def __init__(self, name, label, parameters):
        Component.__init__(self, name, "learner", parameters)
        self.label = label

    def make_model(self):
        raise NotImplementedError()

    def prepare_member(self, member):
        super().prepare_member(member)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        preparations = member.preparations
        learner_name = self.name

        model = self.make_model()
        model_params = model.get_params().keys()
        learner_name = self.name
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(self, member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
        if 'n_jobs' in model_params:
            params['n_jobs'] = -1
        model.set_params(**params)

        if not hasattr(preparations, "steps"):
            preparations.steps = []
        steps = preparations.steps
        steps.append((learner_name, model))
        pipeline = Pipeline(steps=steps)
        preparations.pipeline = pipeline

