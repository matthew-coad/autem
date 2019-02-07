from ..simulators import  Component, Dataset, Role, ChoicesParameter

import sklearn.preprocessing
import sklearn.decomposition
import sklearn.cluster
import sklearn.kernel_approximation

import numpy as np

preprocessor_config_dict = {

    'sklearn.preprocessing.Binarizer': {
        'threshold': np.arange(0.0, 1.01, 0.05)
    },

    'sklearn.decomposition.FastICA': {
        'tol': np.arange(0.0, 1.01, 0.05)
    },

    'sklearn.cluster.FeatureAgglomeration': {
        'linkage': ['ward', 'complete', 'average'],
        'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']
    },

    'sklearn.preprocessing.MaxAbsScaler': {
    },

    'sklearn.preprocessing.MinMaxScaler': {
    },

    'sklearn.preprocessing.Normalizer': {
        'norm': ['l1', 'l2', 'max']
    },

    'sklearn.kernel_approximation.Nystroem': {
        'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        'gamma': np.arange(0.0, 1.01, 0.05),
        'n_components': range(1, 11)
    },

    'sklearn.decomposition.PCA': {
        # 'svd_solver': ['randomized'],
        'iterated_power': range(1, 11)
    },

    'sklearn.preprocessing.PolynomialFeatures': {
        #'degree': [2],
        #'include_bias': [False],
        #'interaction_only': [False]
    },

    'sklearn.kernel_approximation.RBFSampler': {
        'gamma': np.arange(0.0, 1.01, 0.05)
    },

    'sklearn.preprocessing.RobustScaler': {
    },

    'sklearn.preprocessing.StandardScaler': {
    },
}

def get_parameters(config):
    config_dict = preprocessor_config_dict[config]

    def _parameter(key, values):
        return ChoicesParameter(key, [ Role.Configuration ], key, values, None)

    parameters = [ _parameter(k, config_dict[k]) for k in config_dict]
    return parameters

class Preprocesssor(Component):

    def __init__(self, name, label, parameters):
        Component.__init__(self, name, "preprocessor", parameters)
        self.label = label

    def make_preprocessor(self):
        raise NotImplementedError()

    def prepare_member(self, member):
        super().prepare_member(member)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        preparations = member.preparations
        processor_name = self.name

        pre_processor = self.make_preprocessor()
        pre_processor_params = pre_processor.get_params().keys()
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(self, member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
        pre_processor.set_params(**params)

        if not hasattr(preparations, "steps"):
            preparations.steps = []
            
        steps = preparations.steps
        steps.append((processor_name, pre_processor))

class Binarizer(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PBIN", "Binarizer", get_parameters('sklearn.preprocessing.Binarizer'))

    def make_preprocessor(self):
        return sklearn.preprocessing.Binarizer()

class FastICA(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PFIC", "Fast ICA", get_parameters('sklearn.decomposition.FastICA'))

    def make_preprocessor(self):
        return sklearn.decomposition.FastICA()

class FeatureAgglomeration(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PFAG", "Feature Agglomeration", get_parameters('sklearn.cluster.FeatureAgglomeration'))

    def make_preprocessor(self):
        return sklearn.cluster.FeatureAgglomeration()

class MaxAbsScaler(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PMAS", "Max Absolute Scaler", get_parameters('sklearn.preprocessing.MaxAbsScaler'))

    def make_preprocessor(self):
        return sklearn.preprocessing.MaxAbsScaler()

class MinMaxScaler(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PMMS", "Min Max Scaler", get_parameters('sklearn.preprocessing.MinMaxScaler'))

    def make_preprocessor(self):
        return sklearn.preprocessing.MinMaxScaler()

class Normalizer(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PNOR", "Normalizer", get_parameters('sklearn.preprocessing.Normalizer'))

    def make_preprocessor(self):
        return sklearn.preprocessing.Normalizer()

class PCA(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PPCA", "PCA", get_parameters('sklearn.decomposition.PCA'))

    def make_preprocessor(self):
        return sklearn.decomposition.PCA(svd_solver = 'randomized')

class PolynomialFeatures(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PPOF", "Polynomial Features", get_parameters('sklearn.preprocessing.PolynomialFeatures'))

    def make_preprocessor(self):
        return sklearn.preprocessing.PolynomialFeatures(degree=2, include_bias = False, interaction_only = False)

class RBFSampler(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PRBF", "RBF Sampler", get_parameters('sklearn.kernel_approximation.RBFSampler'))

    def make_preprocessor(self):
        return sklearn.kernel_approximation.RBFSampler()

class RobustScaler(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PROB", "Robust Scaler", get_parameters('sklearn.preprocessing.RobustScaler'))

    def make_preprocessor(self):
        return sklearn.preprocessing.RobustScaler()

class StandardScaler(Preprocesssor):

    def __init__(self):
        Preprocesssor.__init__(self, "PSCL", "Standard Scaler", get_parameters('sklearn.preprocessing.StandardScaler'))

    def make_preprocessor(self):
        return sklearn.preprocessing.RobustScaler()
