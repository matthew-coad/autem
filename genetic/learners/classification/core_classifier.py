from ..learner import Learner
from ..parameter import Parameter

from sklearn.linear_model import LogisticRegression as LogisticRegressionModel
from sklearn.tree import DecisionTreeClassifier as DecisionTreeClassifierModel
from sklearn.neighbors import KNeighborsClassifier as KNeighborsClassifierModel
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LinearDiscriminantAnalysisModel
from sklearn.naive_bayes import GaussianNB as GaussianNBModel
from sklearn.svm import SVC as SVCModel

class LogisticRegression(Learner):

    def __init__(self):
        Learner.__init__(self, "LGR", "Logistic Regression", [])

    def make_model(self):
        return LogisticRegressionModel(solver = 'liblinear', multi_class = 'ovr')

class LinearDiscriminantAnalysis(Learner):

    def __init__(self):
        Learner.__init__(self, "LDA", "Linear Discriminant Analysis", [])

    def make_model(self):
        return LinearDiscriminantAnalysisModel()

class KNeighborsClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "KNN", "K-Neighbors Classifier", [])

    def make_model(self):
        return KNeighborsClassifierModel()

class DecisionTreeClassifier(Learner):

    def __init__(self):
        Learner.__init__(self, "CART", "Decision Tree Classifier", [])

    def make_model(self):
        return DecisionTreeClassifierModel()

class GaussianNB(Learner):

    def __init__(self):
        Learner.__init__(self, "NB", "Gaussian Naive Bayes", [])

    def make_model(self):
        return GaussianNBModel()

class SVC(Learner):

    def __init__(self):
        Learner.__init__(self, "SVC", "SVM Classifier", [])

    def make_model(self):
        return SVCModel(gamma='auto')
