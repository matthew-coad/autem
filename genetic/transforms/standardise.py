from .transformer import Transformer
from ..simulators import Dataset, Role

from sklearn.preprocessing import StandardScaler

class Standardise(Transformer):

    def outline_simulation(self, simulation, outline):
        outline.append_attribute("standardise", Dataset.Battle, [ Role.Dimension ], "standardise")

    def start_member(self, member):
        member.configuration.standardise = 1

    def copy_member(self, member, prior):
        member.configuration.standardise = prior.configuration.standardise

    def mutate_member(self, member, prior):
        value = 0 if prior.configuration.standardise == 1 else 1
        member.configuration.standardise = value

    def crossover_member(self, member, parent0, parent1):
        member.configuration.standardise = parent0.configuration.standardise

    def evaluate_member(self, member, evaluation):
        standardise = member.configuration.standardise
        if not hasattr(evaluation, "steps"):
            evaluation.steps = []
        if standardise:
            evaluation.steps.append(('standardise', StandardScaler()))

    def record_member(self, member, record):
        record.standardise = member.configuration.standardise

