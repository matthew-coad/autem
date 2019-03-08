from .. import Group, Dataset, Role, ChoicesParameter

from .preprocessor import Preprocesssor

import sklearn.impute
import sklearn.preprocessing
import sklearn.decomposition
import sklearn.compose
import sklearn.cluster
import sklearn.kernel_approximation
import sklearn.feature_selection
import sklearn.pipeline

import numpy as np

# Engineers

class Engineer(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, label, _convert_config(config))

class NoEngineering(Engineer):

    def __init__(self):
        Engineer.__init__(self, "ENO", "No Engineering", {})

    def make_preprocessor(self, member):
        return None

class PolynomialFeatures(Engineer):

    config = {}

    def __init__(self):
        Engineer.__init__(self, "PLY", "Polynomial Features", self.config)

    def make_preprocessor(self, member):
        return sklearn.preprocessing.PolynomialFeatures(degree=2, include_bias = False, interaction_only = False)
