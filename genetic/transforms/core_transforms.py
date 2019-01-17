from genetic.components import Component

from sklearn.preprocessing import StandardScaler

class StandardiseTransform(Component):

    def initializeMember(self, member):
        standardise = member.simulation.random_state.randint(0, 2)
        member.configuration.standardise = standardise

    def copyMember(self, member, parent0):
        member.configuration.standardise = parent0.configuration.standardise

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.standardise = parent0.configuration.standardise

    def mutateMember(self, member):
        value = 1 if member.configuration.standardise == 0 else 0
        member.configuration.standardise = value

    def evaluateMember(self, member):
        standardise = member.configuration.standardise
        if not hasattr(member.evaluation, "steps"):
            member.evaluation.steps = []
        if standardise:
            member.evaluation.steps.append(('standardise', StandardScaler()))

    def reportMember(self, member, row):
        row.standardise_dim = member.configuration.standardise
