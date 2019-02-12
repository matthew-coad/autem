from ..simulators import  Component, Dataset, Role, ChoicesParameter

import sklearn.preprocessing
import sklearn.decomposition
import sklearn.cluster
import sklearn.kernel_approximation
import sklearn.feature_selection

import numpy as np

def _convert_config(config_dict):
    def _parameter(key, values):
        return ChoicesParameter(key, [ Role.Configuration ], key, values, None)

    parameters = [ _parameter(k, config_dict[k]) for k in config_dict]
    return parameters

class Preprocesssor(Component):

    def __init__(self, name, group, label, config = {}):
        parameters = _convert_config(config)
        Component.__init__(self, name, group, parameters)
        self.label = label

    def make_preprocessor(self):
        raise NotImplementedError()

    def configure_preprocessor(self, member, pre_processor):
        pre_processor_params = pre_processor.get_params().keys()
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(self, member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
        pre_processor.set_params(**params)

    def prepare_member(self, member):
        super().prepare_member(member)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        preparations = member.preparations
        processor_name = self.name
        preprocessor = self.make_preprocessor()
        if preprocessor is None:
            return None

        self.configure_preprocessor(member, preprocessor)
        if not hasattr(preparations, "steps"):
            preparations.steps = []
            
        steps = preparations.steps
        steps.append((processor_name, preprocessor))

# Engineers

class Engineer(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, "Engineer", label, config)

class NoEngineering(Engineer):

    def __init__(self):
        Engineer.__init__(self, "ENO", "No Engineering", {})

    def make_preprocessor(self):
        return None

class PolynomialFeatures(Engineer):

    config = {}

    def __init__(self):
        Engineer.__init__(self, "PLY", "Polynomial Features", self.config)

    def make_preprocessor(self):
        return sklearn.preprocessing.PolynomialFeatures(degree=2, include_bias = False, interaction_only = False)

# Scalers

class Scaler(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, "Scaler", label, config)

class NoScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "SNO", "No Scaling", {})

    def make_preprocessor(self):
        return None

class MaxAbsScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MAS", "Max Absolute Scaler", {})

    def make_preprocessor(self):
        return sklearn.preprocessing.MaxAbsScaler()

class MinMaxScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MMS", "Min Max Scaler", {})

    def make_preprocessor(self):
        return sklearn.preprocessing.MinMaxScaler()

class Normalizer(Scaler):

    config = {
        'norm': ['l1', 'l2', 'max']
    }

    def __init__(self):
        Scaler.__init__(self, "NOR", "Normalizer", self.config)

    def make_preprocessor(self):
        return sklearn.preprocessing.Normalizer()

class RobustScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "RBS", "Robust Scaler", {})

    def make_preprocessor(self):
        return sklearn.preprocessing.RobustScaler()

class StandardScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "SCL", "Standard Scaler", {})

    def make_preprocessor(self):
        return sklearn.preprocessing.RobustScaler()

class Binarizer(Scaler):

    config = {
        'threshold': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Scaler.__init__(self, "BIN", "Binarizer", self.config)

    def make_preprocessor(self):
        return sklearn.preprocessing.Binarizer()

class PowerTransformer(Scaler):

    config = {
        'method': ['yeo-johnson', 'box-cox'],
        'standardize': [True, False]
    }

    def __init__(self):
        Scaler.__init__(self, "PWR", "Power Transform", self.config)

    def make_preprocessor(self):
        return sklearn.preprocessing.PowerTransformer()

# Feature Reducers

class Reducer(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, "Reducer", label, config)

class NoReducer(Reducer):

    def __init__(self):
        Reducer.__init__(self, "RNO", "No Reducer", {})

    def make_preprocessor(self):
        return None

class FastICA(Reducer):

    config = {
        'tol': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Reducer.__init__(self, "FIC", "Fast ICA", self.config)

    def make_preprocessor(self):
        return sklearn.decomposition.FastICA()

class FeatureAgglomeration(Reducer):

    config = {
        'linkage': ['ward', 'complete', 'average'],
        'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']
    }

    def __init__(self):
        Reducer.__init__(self, "FAG", "Feature Agglomeration", self.config)

    def make_preprocessor(self):
        return sklearn.cluster.FeatureAgglomeration()

class PCA(Reducer):

    config = {
        'iterated_power': range(1, 11)
    }

    def __init__(self):
        Reducer.__init__(self, "PCA", "PCA", self.config)

    def make_preprocessor(self):
        return sklearn.decomposition.PCA(svd_solver = 'randomized')

class SelectPercentile(Reducer):

    config = {
        'scorer': ['f_classif', 'mutual_info_classif', 'chi2'],
        'percentile': range(1, 100),
    }

    def __init__(self):
        Reducer.__init__(self, "SPC", "Select Percentile", self.config)

    def make_preprocessor(self):
        scorer = [p for p in self.parameters if p.name == "scorer" ][0]
        percentile = [p for p in self.parameters if p.name == "percentile" ][0]
        score_func = None
        if scorer == "f_classif":
            score_func = sklearn.feature_selection.f_classif
        elif scorer == "mutual_info_classif":
            score_func = sklearn.feature_selection.mutual_info_classif
        elif scorer == "chi2":
            score_func = sklearn.feature_selection.chi2
        selector = sklearn.feature_selection.SelectPercentile(score_func=score_func, percentile=percentile)
        return selector

    def configure_preprocessor(self, member, pre_processor):
        pass


# Approximations

class Approximator(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, "Approximator", label, config)

class NoApproximator(Approximator):

    def __init__(self):
        Approximator.__init__(self, "ANO", "No Approximator", {})

    def make_preprocessor(self):
        return None

class RBFSampler(Approximator):

    config = {
        'gamma': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Approximator.__init__(self, "RBF", "RBF Sampler", self.config)

    def make_preprocessor(self):
        return sklearn.kernel_approximation.RBFSampler()

class Nystroem(Approximator):

    config = {
        'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        'gamma': np.arange(0.0, 1.01, 0.05),
        'n_components': range(1, 11)
    }

    def __init__(self):
        Approximator.__init__(self, "NYS", "Nystroem", self.config)

    def make_preprocessor(self):
        return sklearn.kernel_approximation.Nystroem()

