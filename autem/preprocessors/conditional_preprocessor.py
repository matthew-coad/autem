from .. import Group, Dataset, Role, ChoicesParameter

from .preprocessor import Preprocesssor

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 

import numpy as np

class ConditionalPreprocessor(Preprocesssor):

    def __init__(self, parameters = None):
        if parameters is None:
            config_parameter = ChoicesParameter('strategy', 'strategy', ['mean', 'median'], 'median')
            parameters = [config_parameter]
        Preprocesssor.__init__(self, "CPP", "Conditional Preprocessor", parameters)

    def make_preprocessor(self, member):
        simulation = member.simulation
        loader = simulation.resources.loader
        features = loader.get_features(simulation)

        strategy = self.get_parameter("strategy").get_value(member)
        numeric_features = features['numeric']
        categorical_features = features['nominal']

        # We create the preprocessing pipelines for both numeric and categorical data.

        # We create the preprocessing pipelines for both numeric and categorical data.
        # numeric_features = [0, 1, 2, 5, 6]
        numeric_imputer = SimpleImputer(strategy=strategy)
        numeric_scaler = StandardScaler(copy = True, with_mean=False, with_std=True)
        numeric_transformer = Pipeline(steps=[
            ('imputer', numeric_imputer),
            ('scaler', numeric_scaler)
        ])

        # categorical_features = [3, 4, 7, 8]
        categorical_imputer = SimpleImputer(strategy="most_frequent")
        categorical_encoder = OneHotEncoder(categories='auto', dtype = np.float64, handle_unknown = "error", sparse = True)
        categorical_transformer = Pipeline(steps=[
            ('imputer', categorical_imputer),
            ('encoder', categorical_encoder)
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])
        return preprocessor

    def configure_preprocessor(self, member, pre_processor):
        pass
