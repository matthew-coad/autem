from ..simulators import Parameter, Group, Dataset, Role, Controller

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats

import time

class Learner(Group):

    def __init__(self, name, label, parameters):
        Group.__init__(self, name, parameters)
        self.label = label

    def make_model(self):
        raise NotImplementedError()

    def prepare_member(self, member):
        simulation = member.simulation
        resources = member.resources
        learner_name = self.name

        model = self.make_model()
        model_params = model.get_params().keys()
        learner_name = self.name
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
        if 'n_jobs' in model_params:
            params['n_jobs'] = -1
        model.set_params(**params)

        if not hasattr(resources, "steps"):
            resources.steps = []
        steps = resources.steps
        steps.append((learner_name, model))
        pipeline = Pipeline(steps=steps)
        resources.pipeline = pipeline

