from .hyperLearner import Hyperlearner

from ..choice import Choice
from .. import preprocessors
from ..learners import classification as learners

class ClassificationWide(Hyperlearner):

    def list_components(self):
        components = [
            # Scalers
            Choice("Scaler", [
                preprocessors.StandardScaler()
            ]),


            # Feature Selectors
            Choice("Selector", [
                preprocessors.NoSelector(),
                preprocessors.SelectPercentile(),
                preprocessors.VarianceThreshold()
            ]),

            # Feature Reducers
            Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.PCA(),
            ]),

            # Approximators
            Choice("Approximator", [
                preprocessors.NoApproximator(),
            ]),

            Choice("Learner", [
                learners.GaussianNB(),
                learners.BernoulliNB(),
                learners.MultinomialNB(),
                learners.KNeighborsClassifier(),
                learners.LogisticRegression(),
                learners.LinearSVC(),
                learners.RandomForestClassifier(),
            ])
        ]
        return components

