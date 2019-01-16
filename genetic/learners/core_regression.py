from .learner import Learner
from .parameter import Parameter, ChoiceParameter

from sklearn.linear_model import LinearRegression as LinearRegressionModel
from sklearn.linear_model import Lasso as LassoModel
from sklearn.linear_model import ElasticNet as ElasticNetModel
from sklearn.tree import DecisionTreeRegressor as DecisionTreeRegressorModel
from sklearn.neighbors import KNeighborsRegressor as KNeighborsRegressorModel
from sklearn.svm import SVR as SVRModel

class LinearRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LR", "Linear Regression", [])

    def makeModel(self):
        return LinearRegressionModel()

class KNeighborsRegressor(Learner):

    def __init__(self):
        choices = [3,5,7,9,11,13,15,21,25,31,41,51]
        Learner.__init__(self, "KNN-R", "K-Neighbors", [
            ChoiceParameter("n_neighbors", "n_neighbors_dim", choices)
        ])

    def makeModel(self):
        return KNeighborsRegressorModel()
