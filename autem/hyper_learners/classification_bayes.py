from .hyperLearner import Hyperlearner

from ..choice import Choice
from .. import preprocessors
from ..learners import classification as learners

class ClassificationBayes(Hyperlearner):

    def list_components(self):
        components = [
            # Scalers
            Choice("Scaler", [
                preprocessors.NoScaling(),
            ]),

            # Feature Selectors
            Choice("Selector", [
                preprocessors.NoSelector(),
                preprocessors.SelectPercentile(),
                preprocessors.VarianceThreshold(),
                preprocessors.SelectFwe(),
            ]),

            Choice("Engineer", [
                preprocessors.NoEngineering(),
            ]),

            # Feature Reducers
            Choice("Reducer", [
                preprocessors.NoReducer(),
            ]),

            # Approximators
            Choice("Approximator", [
                preprocessors.NoApproximator(),
            ]),

            Choice("Learner", [
                learners.BernoulliNB(),
                learners.GaussianNB(),
                learners.MultinomialNB(),
            ])
        ]
        return components

