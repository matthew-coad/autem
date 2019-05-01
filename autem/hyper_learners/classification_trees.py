from .hyperLearner import Hyperlearner

from ..choice import Choice
from .. import preprocessors
from ..learners import classification as learners

class ClassificationTrees(Hyperlearner):
    """
    Classification trees hyper-learner.
    """

    def list_components(self):
        components = [
            # Scalers
            Choice("Scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
                preprocessors.BoxCoxTransform(),
                preprocessors.YeoJohnsonTransform(),
            ]),

            # Feature Selectors
            Choice("Selector", [
                preprocessors.NoSelector(),
            ]),

            # Feature Reducers
            Choice("Reducer", [
                preprocessors.NoReducer(),
                preprocessors.FastICA(),
                preprocessors.FeatureAgglomeration(),
                preprocessors.PCA(),
            ]),

            # Approximators
            Choice("Approximator", [
                preprocessors.NoApproximator(),
            ]),

            Choice("Learner", [
                learners.DecisionTreeClassifier(),
                learners.RandomForestClassifier(),
                learners.ExtraTreesClassifier(),
                learners.XGBClassifier(),
            ])
        ]
        return components

