from ..learner import Learner
from ... import Dataset, Role, ChoicesParameter

import sklearn.linear_model 
import sklearn.tree 
import sklearn.neighbors
import sklearn.svm

import numpy as np

def convert_parameters(learner_dict, override_parameters = None):

    if not override_parameters is None:
        return override_parameters

    def _parameter(key, values):
        return ChoicesParameter(key, key, values)

    parameters = [ _parameter(k, learner_dict[k]) for k in learner_dict]
    return parameters

class AdaBoostRegressor(Learner):

    config_dict = {
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'loss': ["linear", "square", "exponential"],
        'max_depth': range(1, 11)
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "ABR", "Ada Boost Regressor", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.ensemble.AdaBoostRegressor(n_estimators=100)

class DecisionTreeRegressor(Learner):

    config_dict = {
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21)
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "DTR", "Decision Tree Regressor", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.tree.DecisionTreeRegressor()

class ElasticNetCV(Learner):

    config_dict = {
        'l1_ratio': np.arange(0.0, 1.01, 0.05),
        'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "ENC", "Elastic Net CV", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.linear_model.ElasticNetCV(cv = 5)

class ExtraTreesRegressor(Learner):

    config_dict = {
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "ETR", "Extra Trees Regressor", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.ensemble.ExtraTreesRegressor(n_estimators=100)

class GradientBoostingRegressor(Learner):

    config_dict = {
        'loss': ["ls", "lad", "huber", "quantile"],
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'subsample': np.arange(0.05, 1.01, 0.05),
        'max_features': np.arange(0.05, 1.01, 0.05),
        'alpha': [0.75, 0.8, 0.85, 0.9, 0.95, 0.99]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "GBR", "Gradient Boosting Regressor", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.ensemble.GradientBoostingRegressor(n_estimators=100)

class LinearRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LR", "Linear Regression", [])

    def make_model(self):
        return sklearn.linear_model.LinearRegression()

class KNeighborsRegressor(Learner):

    config_dict = {
        'n_neighbors': range(1, 101),
        'weights': ["uniform", "distance"],
        'p': [1, 2]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "KNR", "K-Neighbors Regression", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.neighbors.KNeighborsRegressor()

class LassoLarsCV(Learner):

    config_dict = {
        'normalize': [True, False]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "LLC", "Lasso Lars CV", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.linear_model.LassoLarsCV(cv = 5)

class LinearSVR(Learner):

    config_dict = {
        'loss': ["epsilon_insensitive", "squared_epsilon_insensitive"],
        'dual': [True, False],
        'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
        'C': [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.],
        'epsilon': [1e-4, 1e-3, 1e-2, 1e-1, 1.]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "LSR", "Linear SVR", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.svm.LinearSVR()

class RandomForestRegressor(Learner):

    config_dict = {
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "RFR", "Random Forest Regressor", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.ensemble.RandomForestRegressor(n_estimators = 100)

class RidgeCV(Learner):

    config_dict = {
    }

    def __init__(self, parameters = None):
        Learner.__init__(self, "RCV", "Ridge CV", convert_parameters(self.config_dict, parameters))

    def make_model(self):
        return sklearn.linear_model.RidgeCV(cv = 5)

#    'xgboost.XGBRegressor': {
#        'n_estimators': [100],
#        'max_depth': range(1, 11),
#        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
#        'subsample': np.arange(0.05, 1.01, 0.05),
#        'min_child_weight': range(1, 21),
#        'nthread': [1]
#    }
