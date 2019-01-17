from genetic.components import Component
from .parameter import Parameter

from types import SimpleNamespace

class Learner(Component):

    def __init__(self, name, label, parameters):
        self.name = name
        self.label = label
        self.parameters = parameters

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
            params = dict([(p.name, p.getMemberValue(self, member)) for p in self.parameters])
            model.set_params(**params)
        member.evaluation.model = model
        member.evaluation.model_name = self.name

    def reportMember(self, member, row):
        if not self.isActive(member):
            return None

        for parameter in self.parameters:
            parameter.reportParameter(self, member, row)

        row.model_dim = member.evaluation.model_name

