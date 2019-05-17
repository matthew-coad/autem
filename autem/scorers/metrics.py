import sklearn.metrics

def neg_mean_squared_error(y_true, y_pred):
    return 0 - sklearn.metrics.mean_squared_error(y_true, y_pred)

def accuracy_score(y_true, y_pred):
    return sklearn.metrics.accuracy_score(y_true, y_pred)
