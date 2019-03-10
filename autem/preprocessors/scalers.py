from .. import Group, Dataset, Role, ChoicesParameter, make_choice_list

from .preprocessor import Preprocesssor

import sklearn.impute as impute
import sklearn.preprocessing as preprocessing
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 

import pandas as pd
import numpy as np

class Scaler(Preprocesssor):

    def __init__(self, name, label, parameters):
        config_parameter = ChoicesParameter('num__imp__strategy', 'strategy', ['mean', 'median'], True)
        parameters = [config_parameter] + parameters
        Preprocesssor.__init__(self, name, label, parameters)

    def make_scaler(self, member):
        raise NotImplementedError()

    def make_preprocessor(self, member):
        simulation = member.simulation
        loader = simulation.resources.loader
        features = loader.get_features(simulation)

        categorical_features = features['nominal']
        numeric_features = features['numeric']

        x,y = loader.load_divided_data(simulation)

        categories = []
        for feature in categorical_features:
            values = np.unique(x[:,feature])
            values = values[~np.isnan(values)]
            values = np.sort(values)
            categories.append(values)

        # We create the preprocessing pipelines for both numeric and categorical data.

        # We create the preprocessing pipelines for both numeric and categorical data.
        # numeric_features = [0, 1, 2, 5, 6]
        numeric_imputer = impute.SimpleImputer(strategy='median')
        numeric_scaler = self.make_scaler(member)
        numeric_transformer = Pipeline(steps=[
            ('imp', numeric_imputer),
            ('scaler', numeric_scaler)
        ])

        # categorical_features = [3, 4, 7, 8]
        categorical_imputer = impute.SimpleImputer(strategy="most_frequent")
        categorical_encoder = preprocessing.OneHotEncoder(categories=categories, dtype = np.float64, handle_unknown = "error", sparse=False)
        categorical_transformer = Pipeline(steps=[
            ('imp', categorical_imputer),
            ('enc', categorical_encoder)
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])
        return preprocessor

#class MissingIndicatorImputer(Imputer):
#
#    def __init__(self):
#        # config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median', 'most_frequent'], 'median')
#        config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median'], 'median')
#        Imputer.__init__(self, "MII", "Missing Indicator Imputer", [config_parameter])

#    def make_preprocessor(self, member):
#        return sklearn.impute.SimpleImputer()

#    def make_preprocessor(self, member):
#        strategy_param = [p for p in self.parameters if p.name == "strategy" ][0]
#        strategy = strategy_param.get_value(member)

#        transformer = sklearn.pipeline.FeatureUnion(
#            transformer_list=[
#                ('features', sklearn.impute.SimpleImputer(strategy=strategy)),
#                ('indicators', sklearn.impute.MissingIndicator())])
#        return transformer

#    def configure_preprocessor(self, member, pre_processor):
#        pass

# Scalers

class MaxAbsScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MAS", "Max Absolute Scaler", [])

    def make_scaler(self, member):
        return preprocessing.MaxAbsScaler()

class MinMaxScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "MMS", "Min Max Scaler", [])

    def make_scaler(self, member):
        return preprocessing.MinMaxScaler()

class Normalizer(Scaler):

    config = {
        'num__scaler__norm': ['l1', 'l2', 'max']
    }

    def __init__(self):
        Scaler.__init__(self, "NOR", "Normalizer", make_choice_list(self.config))

    def make_scaler(self, member):
        return preprocessing.Normalizer()

class RobustScaler(Scaler):

    def __init__(self):
        Scaler.__init__(self, "RBS", "Robust Scaler", [])

    def make_scaler(self, member):
        return preprocessing.RobustScaler()

class StandardScaler(Scaler):

    config = {
        'num__scaler__with_mean': [True, False]
    }

    def __init__(self):
        Scaler.__init__(self, "SCL", "Standard Scaler", make_choice_list(self.config))

    def make_scaler(self, member):
        return preprocessing.StandardScaler(copy = True, with_mean=True, with_std=True)

class Binarizer(Scaler):

    config = {
        'num__scaler__threshold': np.arange(0.0, 1.01, 0.05)
    }

    def __init__(self):
        Scaler.__init__(self, "BIN", "Binarizer", make_choice_list(self.config))

    def make_scaler(self, member):
        return preprocessing.Binarizer()
        
class BoxCoxTransform(Scaler):

    def __init__(self):
        Scaler.__init__(self, "BXC", "Box-Cox Transform", [])

    def make_scaler(self, member):
        return preprocessing.PowerTransformer(method = "box-cox", standardize=True)

class YeoJohnsonTransform(Scaler):

    def __init__(self):
        Scaler.__init__(self, "YJH", "Yeo-Johnson Transform", [])

    def make_scaler(self, member):
        return preprocessing.PowerTransformer(method = "yeo-johnson", standardize=True)
