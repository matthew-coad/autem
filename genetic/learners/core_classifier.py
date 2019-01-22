from .learner import Learner
from .parameter import Parameter

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from sklearn.tree import DecisionTreeClassifier as DecisionTreeClassifierModel
from sklearn.neighbors import KNeighborsClassifier as KNeighborsClassifierModel
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LinearDiscriminantAnalysisModel
from sklearn.naive_bayes import GaussianNB as GaussianNBModel
from sklearn.svm import SVC as SVCModel

class LogisticRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LGR", "Logistic Regression", [])

    def makeModel(self):
        return LogisticRegressionModel(solver = 'liblinear', multi_class = 'ovr')


