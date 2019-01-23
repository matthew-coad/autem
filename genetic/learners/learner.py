from ..simulators import Component, Evaluation, Dataset, Role
from .parameter import Parameter

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats


class Learner(Component):

    def __init__(self, name, label, parameters):
        self.name = name
        self.label = label
        self.parameters = parameters

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        if not outline.has_attribute("test_score", Dataset.Battle):
            outline.append_attribute("learner_name", Dataset.Battle, [ Role.Dimension ], "model")
            outline.append_attribute("test_score", Dataset.Battle, [ Role.Measure ], "score")

    def start_member(self, member):
        configuration = member.configuration
        if not hasattr(configuration, "learners"):
            configuration.learners = SimpleNamespace()
        setattr(configuration.learners, self.name, SimpleNamespace())
        all_learners = list(member.configuration.learners.__dict__)
        random_state = member.simulation.random_state
        learner_index = random_state.randint(0, len(all_learners))
        member.configuration.learner_name = all_learners[learner_index]

    def make_model(self):
        return self.makeModel()

    def is_active(self, member):
        learner_name = member.configuration.learner_name
        active = learner_name == self.name
        return active

    def evaluate_member(self, member, evaluation):
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

        steps = []
        steps.append((learner_name, model))
        pipeline = Pipeline(steps=steps)

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        test_score = scorer.score(y_test, y_pred)

        evaluation.learner_name = learner_name
        evaluation.test_score = test_score

    def record_member(self, member, record):
        if not self.is_active(member):
            return None

        test_score = None
        learner_name = None

        test_scores = np.array([e.test_score for e in member.evaluations])
        if len(member.evaluations) > 0:
            test_score = test_scores.mean()
            learner_name = member.evaluations[-1].learner_name
        
        record.test_score = test_score
        record.learner_name = learner_name

    def makeModel(self):
        raise NotImplementedError()
