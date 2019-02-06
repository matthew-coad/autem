from ..learner import Learner
from ...simulators import Dataset, Role, ChoicesParameter

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from sklearn.tree import DecisionTreeClassifier as DecisionTreeClassifierModel
from sklearn.neighbors import KNeighborsClassifier as KNeighborsClassifierModel
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LinearDiscriminantAnalysisModel
from sklearn.naive_bayes import GaussianNB as GaussianNBModel
from sklearn.svm import SVC as SVCModel

import numpy as np

classifier_config_dict = {

    # Classifiers
    'sklearn.naive_bayes.GaussianNB': {
    },

    'sklearn.naive_bayes.BernoulliNB': {
        'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
        'fit_prior': [True, False]
    },

    'sklearn.naive_bayes.MultinomialNB': {
        'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
        'fit_prior': [True, False]
    },

    'sklearn.tree.DecisionTreeClassifier': {
        'criterion': ["gini", "entropy"],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21)
    },

    'sklearn.ensemble.ExtraTreesClassifier': {
        'n_estimators': [100],
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    },

    'sklearn.ensemble.RandomForestClassifier': {
        'n_estimators': [100],
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf':  range(1, 21),
        'bootstrap': [True, False]
    },

    'sklearn.ensemble.GradientBoostingClassifier': {
        'n_estimators': [100],
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'subsample': np.arange(0.05, 1.01, 0.05),
        'max_features': np.arange(0.05, 1.01, 0.05)
    },

    'sklearn.neighbors.KNeighborsClassifier': {
        'n_neighbors': range(1, 101),
        'weights': ["uniform", "distance"],
        'p': [1, 2]
    },

    'sklearn.svm.LinearSVC': {
        'penalty': ["l1", "l2"],
        'loss': ["hinge", "squared_hinge"],
        'dual': [True, False],
        'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
        'C': [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.]
    },

    'sklearn.linear_model.LogisticRegression': {
        'penalty': ["l1", "l2"],
        'C': [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.],
        'dual': [True, False]
    },

    'xgboost.XGBClassifier': {
        'n_estimators': [100],
        'max_depth': range(1, 11),
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'subsample': np.arange(0.05, 1.01, 0.05),
        'min_child_weight': range(1, 21),
        'nthread': [1]
    }

}

def get_parameters(config):
    learner_dict = classifier_config_dict[config]

    def _parameter(key, values):
        return ChoicesParameter(key, [ Role.Configuration ], key, values, None)

    parameters = [ _parameter(k, learner_dict[k]) for k in learner_dict]
    return parameters

class LogisticRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LGR", "Logistic Regression", get_parameters('sklearn.linear_model.LogisticRegression'))

    def make_model(self):
        return LogisticRegressionModel(solver = 'liblinear', multi_class = 'ovr')

class LinearDiscriminantAnalysis(Learner):

    def __init__(self):
        Learner.__init__(self, "LDA", "Linear Discriminant Analysis", [])

    def make_model(self):
        return LinearDiscriminantAnalysisModel()

class KNeighborsClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "KNN", "K-Neighbors Classifier", get_parameters('sklearn.neighbors.KNeighborsClassifier'))

    def make_model(self):
        return KNeighborsClassifierModel()

class DecisionTreeClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "CART", "Decision Tree Classifier", get_parameters('sklearn.tree.DecisionTreeClassifier'))

    def make_model(self):
        return DecisionTreeClassifierModel()

class GaussianNB(Learner):

    def __init__(self):
        Learner.__init__(self, "NB", "Gaussian Naive Bayes", get_parameters('sklearn.naive_bayes.GaussianNB'))

    def make_model(self):
        return GaussianNBModel()

class SVC(Learner):

    def __init__(self):
        Learner.__init__(self, "SVC", "SVM Classifier", get_parameters('sklearn.svm.LinearSVC'))

    def make_model(self):
        return SVCModel(gamma='auto')
