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


# Feature Reducers

class Reducer(Preprocesssor):

    def __init__(self, name, label, parameters):
        Preprocesssor.__init__(self, name, label, parameters)

class NoReducer(Reducer):

    def __init__(self):
        Reducer.__init__(self, "RNO", "No Reducer", [])

    def make_preprocessor(self, member):
        return None

class FastICA(Reducer):

    config = {
        'numeric': {
            'tol': np.arange(0.0, 1.01, 0.05)
        }
    }

    def __init__(self):
        Reducer.__init__(self, "FIC", "Fast ICA", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.decomposition.FastICA(tol = 0.05)

class FeatureAgglomeration(Reducer):

    config = {
        'nominal': {
            'linkage': ['ward', 'complete', 'average'],
            'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']
        },
    }

    def __init__(self):
        Reducer.__init__(self, "FAG", "Feature Agglomeration", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.cluster.FeatureAgglomeration()

class PCA(Reducer):

    config = {
        'numeric': {
            'iterated_power': range(1, 11)
        },
    }

    def __init__(self):
        Reducer.__init__(self, "PCA", "PCA", make_choice_list(self.config))

    def make_preprocessor(self, member):
        return sklearn.decomposition.PCA(svd_solver = 'randomized', iterated_power=3)
