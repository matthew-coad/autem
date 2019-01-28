from ..simulators import Parameter, Component, Evaluation, Dataset, Role

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats


class Learner(Component):

    def __init__(self, name, label, parameters):
        Component.__init__(self, name, "learner", parameters)
        self.label = label

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        super().outline_simulation(simulation, outline)
        if not outline.has_attribute("test_score", Dataset.Battle):
            outline.append_attribute("test_score", Dataset.Battle, [ Role.Measure ], "score")

    def make_model(self):
        raise NotImplementedError()

    def evaluate_member(self, member, evaluation):
        super().evaluate_member(member, evaluation)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        member_id = member.id
        random_state = simulation.random_state

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_divided()
        test_size = 0.3
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

        model = self.make_model()
        learner_name = self.name
        #if len(self.parameters) > 0:
        #   pairs = [(p.name, p.getMemberValue(self, member)) for p in self.parameters]
        #    params = dict(p for p in pairs if not p[1] is None)
        #    model.set_params(**params)

        if hasattr(evaluation, "steps"):
            steps = evaluation.steps
        else:
            steps = []

        steps.append((learner_name, model))
        pipeline = Pipeline(steps=steps)

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        test_score = scorer.score(y_test, y_pred)

        evaluation.test_score = test_score

    def record_member(self, member, record):
        super().record_member(member, record)

        if not self.is_active(member):
            return None

        record.test_score = None
        if member.evaluations:
            test_scores = np.array([e.test_score for e in member.evaluations])
            record.test_score = test_scores.mean()

