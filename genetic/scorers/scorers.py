from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score


def neg_mean_squared_error_scorer(y_true, y_pred):
    return 0 - mean_squared_error(y_true, y_pred)

def accuracy_scorer(y_true, y_pred):
    return accuracy_score(y_true, y_pred)
