from ..learner import Learner
from ... import Dataset, Role, ChoicesParameter

import sklearn.linear_model
import sklearn.neighbors
import sklearn.discriminant_analysis
import sklearn.svm
import sklearn.naive_bayes
import sklearn.tree
import sklearn.ensemble
# import sklearn.xgboost

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
        #'n_estimators': [100],
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        #'bootstrap': [True, False]
    },

    'sklearn.ensemble.RandomForestClassifier': {
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf':  range(1, 21),
        #'bootstrap': [True, False]
    },

    'sklearn.ensemble.GradientBoostingClassifier': {
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
        # 'penalty': ["l1", "l2"],
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
        return ChoicesParameter(key, key, values, None)

    parameters = [ _parameter(k, learner_dict[k]) for k in learner_dict]
    return parameters

class GaussianNB(Learner):

    def __init__(self):
        Learner.__init__(self, "GNB", "Gaussian Naive Bayes", get_parameters('sklearn.naive_bayes.GaussianNB'))

    def make_model(self):
        return sklearn.naive_bayes.GaussianNB()

class BernoulliNB(Learner):

    def __init__(self):
        Learner.__init__(self, "BNB", "Bernoulli Naive-Bayes", get_parameters('sklearn.naive_bayes.BernoulliNB'))

    def make_model(self):
        return sklearn.naive_bayes.BernoulliNB()

class MultinomialNB(Learner):

    def __init__(self):
        Learner.__init__(self, "MNB", "Multinomial Naive-Bayes", get_parameters('sklearn.naive_bayes.MultinomialNB'))

    def make_model(self):
        return sklearn.naive_bayes.MultinomialNB()

class DecisionTreeClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "CART", "Decision Tree Classifier", get_parameters('sklearn.tree.DecisionTreeClassifier'))

    def make_model(self):
        return sklearn.tree.DecisionTreeClassifier()

class ExtraTreesClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "EXT", "Extra Trees", get_parameters('sklearn.ensemble.ExtraTreesClassifier'))

    def make_model(self):
        return sklearn.tree.ExtraTreeClassifier()

class RandomForestClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "RF", "Random Forests", get_parameters('sklearn.ensemble.RandomForestClassifier'))

    def make_model(self):
        return sklearn.ensemble.RandomForestClassifier(n_estimators = 100)

class GradientBoostingClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "GB", "Gradient Boosting", get_parameters('sklearn.ensemble.GradientBoostingClassifier'))

    def make_model(self):
        return sklearn.ensemble.GradientBoostingClassifier(n_estimators = 100)

class KNeighborsClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "KNN", "K-Neighbors Classifier", get_parameters('sklearn.neighbors.KNeighborsClassifier'))

    def make_model(self):
        return sklearn.neighbors.KNeighborsClassifier()

class LinearSVC(Learner):

    def __init__(self):
        Learner.__init__(self, "LSV", "Linear SVC", get_parameters('sklearn.svm.LinearSVC'))

    def make_model(self):
        return sklearn.svm.LinearSVC()

class LogisticRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LGR", "Logistic Regression", get_parameters('sklearn.linear_model.LogisticRegression'))

    def make_model(self):
        return sklearn.linear_model.LogisticRegression(solver =  'lbfgs', multi_class = 'ovr')

class LinearDiscriminantAnalysis(Learner):

    def __init__(self):
        Learner.__init__(self, "LDA", "Linear Discriminant Analysis", [])

    def make_model(self):
        return sklearn.discriminant_analysis.LinearDiscriminantAnalysis()
