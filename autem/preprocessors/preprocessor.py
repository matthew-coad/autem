from .. import Group, Dataset, Role, ChoicesParameter

import sklearn.impute
import sklearn.preprocessing
import sklearn.decomposition
import sklearn.cluster
import sklearn.kernel_approximation
import sklearn.feature_selection
import sklearn.pipeline

import numpy as np

def _convert_config(config_dict):
    def _parameter(key, values):
        return ChoicesParameter(key, key, values, None)

    parameters = [ _parameter(k, config_dict[k]) for k in config_dict]
    return parameters

class Preprocesssor(Group):

    def __init__(self, name, label, parameters):
        Group.__init__(self, name, parameters)
        self.label = label

    def make_preprocessor(self, member):
        raise NotImplementedError()

    def configure_preprocessor(self, member, pre_processor):
        pre_processor_params = pre_processor.get_params().keys()
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
            pre_processor.set_params(**params)

    def prepare_member(self, member):
        super().prepare_member(member)

        simulation = member.simulation
        resources = member.resources
        processor_name = self.name
        preprocessor = self.make_preprocessor(member)
        if preprocessor is None:
            return None

        self.configure_preprocessor(member, preprocessor)
        if not hasattr(resources, "steps"):
            resources.steps = []
            
        steps = resources.steps
        steps.append((processor_name, preprocessor))

# Imputers

class Imputer(Preprocesssor):

    def __init__(self, name, label, parameters):
        Preprocesssor.__init__(self, name, label, parameters)

class NoImputer(Imputer):

    def __init__(self):
        Imputer.__init__(self, "INO", "No Imputer", [])

    def make_preprocessor(self, member):
        return None

class SimpleImputer(Imputer):

    def __init__(self, parameters = None):
        if parameters is None:
            # config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median', 'most_frequent'], 'median')
            config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median'], 'median')
            parameters = [config_parameter]
        Imputer.__init__(self, "SMP", "Simple Imputer", parameters)

    def make_preprocessor(self, member):
        return sklearn.impute.SimpleImputer()

class MissingIndicatorImputer(Imputer):

    def __init__(self):
        # config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median', 'most_frequent'], 'median')
        config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median'], 'median')
        Imputer.__init__(self, "MII", "Missing Indicator Imputer", [config_parameter])

    def make_preprocessor(self, member):
        return sklearn.impute.SimpleImputer()

    def make_preprocessor(self, member):
        strategy_param = [p for p in self.parameters if p.name == "strategy" ][0]
        strategy = strategy_param.get_value(member)

        transformer = sklearn.pipeline.FeatureUnion(
            transformer_list=[
                ('features', sklearn.impute.SimpleImputer(strategy=strategy)),
                ('indicators', sklearn.impute.MissingIndicator())])
        return transformer

    def configure_preprocessor(self, member, pre_processor):
        pass

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

# Scalers

class Scaler(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, label, _convert_config(config))

class NoScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "SNO", "No Scaling", {})

    def make_preprocessor(self, member):
        return None

class MaxAbsScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MAS", "Max Absolute Scaler", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.MaxAbsScaler()

class MinMaxScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MMS", "Min Max Scaler", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.MinMaxScaler()

class Normalizer(Scaler):

    config = {
        'norm': ['l1', 'l2', 'max']
    }

    def __init__(self, config = None):
        if config is None:
            config = self.config
        Scaler.__init__(self, "NOR", "Normalizer", config)

    def make_preprocessor(self, member):
        return sklearn.preprocessing.Normalizer()

class RobustScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "RBS", "Robust Scaler", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.RobustScaler()

class StandardScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "SCL", "Standard Scaler", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.StandardScaler()

class Binarizer(Scaler):

    config = {
        'threshold': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Scaler.__init__(self, "BIN", "Binarizer", self.config)

    def make_preprocessor(self, member):
        return sklearn.preprocessing.Binarizer()
        
class PowerTransformer(Scaler):

    config = {
        'method': ['yeo-johnson', 'box-cox'],
        'standardize': [True, False]
    }

    def __init__(self):
        Scaler.__init__(self, "PWR", "Power Transform", self.config)

    def make_preprocessor(self, member):
        return sklearn.preprocessing.PowerTransformer()

class BoxCoxTransform(Scaler):

    def __init__(self):
        Scaler.__init__(self, "BXC", "Box-Cox Transform", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.PowerTransformer(method = "box-cox", standardize=True)

class YeoJohnsonTransform(Scaler):

    def __init__(self):
        Scaler.__init__(self, "YJH", "Yeo-Johnson Transform", {})

    def make_preprocessor(self, member):
        return sklearn.preprocessing.PowerTransformer(method = "yeo-johnson", standardize=True)



# Feature Reducers

class Reducer(Preprocesssor):

    def __init__(self, name, label, config):
        Preprocesssor.__init__(self, name, label, _convert_config(config))

class NoReducer(Reducer):

    def __init__(self):
        Reducer.__init__(self, "RNO", "No Reducer", {})

    def make_preprocessor(self, member):
        return None

class FastICA(Reducer):

    config = {
        'tol': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Reducer.__init__(self, "FIC", "Fast ICA", self.config)

    def make_preprocessor(self, member):
        return sklearn.decomposition.FastICA()

class FeatureAgglomeration(Reducer):

    config = {
        'linkage': ['ward', 'complete', 'average'],
        'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']
    }

    def __init__(self):
        Reducer.__init__(self, "FAG", "Feature Agglomeration", self.config)

    def make_preprocessor(self, member):
        return sklearn.cluster.FeatureAgglomeration()

class PCA(Reducer):

    config = {
        'iterated_power': range(1, 11)
    }

    def __init__(self):
        Reducer.__init__(self, "PCA", "PCA", self.config)

    def make_preprocessor(self, member):
        return sklearn.decomposition.PCA(svd_solver = 'randomized')

class SelectPercentile(Preprocesssor):

    def __init__(self):
        scorer_parameter = ChoicesParameter("scorer", "scorer", ['f_classif', 'mutual_info_classif', 'chi2'], 'f_classif')
        percentile_parameter = ChoicesParameter("percentile", "percentile", [1,2,5,10,20,30,40,50,60,70,80,90,95,100], 10)
        Preprocesssor.__init__(self, "SPC", "Select Percentile", [scorer_parameter, percentile_parameter])

    def make_preprocessor(self, member):
        scorer_param = [p for p in self.parameters if p.name == "scorer" ][0]
        percentile_param = [p for p in self.parameters if p.name == "percentile" ][0]
        scorer = scorer_param.get_value(member)
        percentile = percentile_param.get_value(member)
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
        Preprocesssor.__init__(self, name, label, _convert_config(config))

class NoApproximator(Approximator):

    def __init__(self):
        Approximator.__init__(self, "ANO", "No Approximator", {})

    def make_preprocessor(self, member):
        return None

class RBFSampler(Approximator):

    config = {
        'gamma': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Approximator.__init__(self, "RBF", "RBF Sampler", self.config)

    def make_preprocessor(self, member):
        return sklearn.kernel_approximation.RBFSampler()

class Nystroem(Approximator):

    config = {
        'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        'gamma': np.arange(0.0, 1.01, 0.05),
        'n_components': range(1, 11)
    }

    def __init__(self):
        Approximator.__init__(self, "NYS", "Nystroem", self.config)

    def make_preprocessor(self, member):
        return sklearn.kernel_approximation.Nystroem()

