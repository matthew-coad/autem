from ..group import Group
from ..reporters import DataType, Role
from ..choices_parameter import ChoicesParameter, make_choice, make_choice_list
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

    def __init__(self, name, label, parameters):
        Preprocesssor.__init__(self, name, label, parameters)

class NoEngineering(Engineer):

    def __init__(self):
        Engineer.__init__(self, "ENO", "No Engineering", [])

    def make_preprocessor(self, member):
        return None

class PolynomialFeatures(Engineer):

    config = {
        'nominal': {
            'degree': [2, 3],
            'include_bias': [True, False],
            'interaction_only': [True, False]
        }
    }

    def __init__(self):
        Engineer.__init__(self, "PLY", "Polynomial Features", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.preprocessing.PolynomialFeatures()

    