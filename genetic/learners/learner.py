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

    def evaluate_member(self, member):
        super().evaluate_member(member)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        preparations = member.preparations
        evaluation = member.evaluation
        random_state = simulation.random_state

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        start = time.time()

        x,y = loader.load_divided()
        test_size = 0.3
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

        end = time.time()
        duration = end - start

        pipeline = preparations.pipeline
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        test_score = scorer.score(y_test, y_pred)
        member.accuracy_measured(test_score)
        member.duration_measured(duration)

