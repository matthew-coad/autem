from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score

from .scorer import Scorer


def neg_mean_squared_error_scorer(y_true, y_pred):
    return 0 - mean_squared_error(y_true, y_pred)

def accuracy_scorer(y_true, y_pred):
    return accuracy_score(y_true, y_pred)

class NegativeRMSE(Scorer):

    def __init__(self):
        Scorer.__init__(self, "NegativeRMSE")

    def score(self, y_true, y_pred):
        return 0 - mean_squared_error(y_true, y_pred)

class Accuracy(Scorer):

    def __init__(self):
        Scorer.__init__(self, "Accuracy")

    def score(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)
