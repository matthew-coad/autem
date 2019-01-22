from genetic.components import Component
from ..simulators import Component as Component2, Evaluation
from .parameter import Parameter

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from scipy import stats


class Learner(Component, Component2):

    def __init__(self, name, label, parameters):
        self.name = name
        self.label = label
        self.parameters = parameters

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
        model_name = self.name
        #if len(self.parameters) > 0:
        #   pairs = [(p.name, p.getMemberValue(self, member)) for p in self.parameters]
        #    params = dict(p for p in pairs if not p[1] is None)
        #    model.set_params(**params)

        steps = []
        steps.append((model_name, model))
        pipeline = Pipeline(steps=steps)

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        test_score = scorer.score(y_test, y_pred)

        evaluation.test_score = test_score

    def makeModel(self):
        raise NotImplementedError()

    def initializeMember(self, member):
        configuration = member.configuration
        if not hasattr(configuration, "learners"):
            configuration.learners = SimpleNamespace()
        setattr(configuration.learners, self.name, SimpleNamespace())
        for parameter in self.parameters:
            parameter.initializeParameter(self, member)

    def copyMember(self, member, parent0):
        configuration = member.configuration
        if not hasattr(configuration, "learners"):
            configuration.learners = SimpleNamespace()
        setattr(configuration.learners, self.name, SimpleNamespace())
        for parameter in self.parameters:
            parameter.copyParameter(self, member, parent0)

    def crossoverMember(self, member, parent0, parent1):
        configuration = member.configuration
        if not hasattr(configuration, "learners"):
            configuration.learners = SimpleNamespace()
        setattr(configuration.learners, self.name, SimpleNamespace())
        for parameter in self.parameters:
            parameter.crossoverParameter(self, member, parent0, parent1)

    def mutateMember(self, member):
        if not self.isActive(member):
            return False

        random_state = member.simulation.random_state
        parameters = self.parameters
        n_parameter = len(parameters)
        if n_parameter == 0:
            return False

        parameter_indexes = random_state.choice(n_parameter, size = n_parameter, replace = False)
        parameter = parameters[parameter_indexes[0]]
        parameter.mutateParameter(self, member)
        return True

    def isActive(self, member):
        configuration = member.configuration
        if hasattr(configuration, "learner_name"):
            learner_name = getattr(configuration, "learner_name")
        else:
            learner_name = self.name
        active = learner_name == self.name
        return active

    def evaluateMember(self, member):
        if not self.isActive(member):
            return None

        model = self.makeModel()
        if len(self.parameters) > 0:
            pairs = [(p.name, p.getMemberValue(self, member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
            model.set_params(**params)
        member.evaluation.model = model
        member.evaluation.model_name = self.name

    def reportMember(self, member, row):
        if not self.isActive(member):
            return None

        for parameter in self.parameters:
            parameter.reportParameter(self, member, row)

        row.model_dim = member.evaluation.model_name

