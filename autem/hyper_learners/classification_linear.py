from .hyperLearner import Hyperlearner

from ..choice import Choice
from .. import preprocessors
from ..learners import classification as learners

class ClassificationLinear(Hyperlearner):

    def list_components(self):
        components = [
            # Scalers
            Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.Binarizer(),
                preprocessors.BoxCoxTransform(),
                preprocessors.YeoJohnsonTransform()
            ]),

            # Feature Selectors
            Choice("Selector", [
                preprocessors.NoSelector(),
                preprocessors.SelectPercentile(),
                preprocessors.VarianceThreshold()
            ]),

            Choice("Engineer", [
                preprocessors.NoEngineering(),
            ]),

            # Feature Reducers
            Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.FastICA(),
                preprocessors.PCA(),
            ]),

            # Approximators
            Choice("Approximator", [
                preprocessors.NoApproximator(),
            ]),

            Choice("Learner", [
                learners.LogisticRegression(),
                learners.LinearDiscriminantAnalysis(),
            ])
        ]
        return components

