from .. import Group, Dataset, Role, ChoicesParameter, make_choice_list

import sklearn.impute
import sklearn.preprocessing
import sklearn.decomposition
import sklearn.compose
import sklearn.cluster
import sklearn.kernel_approximation
import sklearn.feature_selection
import sklearn.pipeline

import numpy as np

from .preprocessor import Preprocesssor

# Approximations

class Approximator(Preprocesssor):

    def __init__(self, name, label, parameters):
        Preprocesssor.__init__(self, name, label, parameters)

class NoApproximator(Approximator):

    def __init__(self):
        Approximator.__init__(self, "ANO", "No Approximator", [])

    def make_preprocessor(self, member):
        return None

class RBFSampler(Approximator):

    config = {
        'numeric': {
            'gamma': np.arange(0.0, 1.01, 0.05)
        }
    }

    def __init__(self):
        Approximator.__init__(self, "RBF", "RBF Sampler", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.kernel_approximation.RBFSampler()

class Nystroem(Approximator):

    config = {
        'nominal': {
            'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        },
        'numeric': {
            'gamma': np.arange(0.0, 1.01, 0.05),
            'n_components': range(1, 11)
        }
    }

    def __init__(self):
        Approximator.__init__(self, "NYS", "Nystroem", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.kernel_approximation.Nystroem()
