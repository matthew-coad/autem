from .transformer import Transformer
from ..simulators import ChoicesParameter, Dataset, Role

from sklearn.preprocessing import StandardScaler

class Standardise(Transformer):

    def __init__(self):
        Transformer.__init__(self, "standardise", None, [
            ChoicesParameter("active", [Role.Configuration], "standardise", [0,1], 1)
        ])

    def evaluate_member(self, member, evaluation):
        standardise = member.configuration.standardise.active
        if not hasattr(evaluation, "steps"):
            evaluation.steps = []
        if standardise:
            evaluation.steps.append((self.name, StandardScaler()))
