from ..simulators import Parameter, Component, Dataset, Role

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats


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

        model = self.make_model()
        learner_name = self.name
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(self, member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
            model.set_params(**params)

        preparations.model = model

    def evaluate_member(self, member):
        super().evaluate_member(member)
        if not self.is_active(member):
            return None

        member_id = member.id
        learner_name = self.name
        simulation = member.simulation
        preparations = member.preparations
        evaluation = member.evaluation
        random_state = simulation.random_state

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_divided()
        test_size = 0.3
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

        model = preparations.model
        if hasattr(preparations, "steps"):
            steps = preparations.steps
        else:
            steps = []

        steps.append((learner_name, model))
        pipeline = Pipeline(steps=steps)
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        test_score = scorer.score(y_test, y_pred)
        member.accuracy_measured(test_score)

