if __name__ == '__main__':
    import context

import benchmark.replications.replicator as replicator

import sklearn.pipeline as pipelines
import sklearn.model_selection as model_selection
import sklearn.impute as impute
import sklearn.preprocessing as preprocessing
import sklearn.svm as svm
import sklearn.feature_selection as feature_selection
import sklearn.model_selection as model_selection

import numpy as np
 
# From openml
# sklearn.pipeline.Pipeline(
#     columntransformer=sklearn.compose._column_transformer.ColumnTransformer(
#         numeric=sklearn.pipeline.Pipeline(
#             imputer=sklearn.preprocessing.imputation.Imputer,
#             standardscaler=sklearn.preprocessing.data.StandardScaler),
#         nominal=sklearn.pipeline.Pipeline(
#             simpleimputer=sklearn.impute.SimpleImputer,
#             onehotencoder=sklearn.preprocessing._encoders.OneHotEncoder)
#     ),
#     variancethreshold=sklearn.feature_selection.variance_threshold.VarianceThreshold,
#     svc=sklearn.svm.classes.SVC
# )

def make_cylinder_bands_pipeline(x, y, features):
    return pipeline
    

def run_replication():
    print("Running cylinder_bands replication")
    dataset = replicator.get_dataset(6332)
    x, y = replicator.get_data(dataset)
    features = replicator.get_features(dataset)
    categories = replicator.get_one_hot_categories(x, features)

    # NumericImputer copy true
    # NumericImputer fill_value -1
    # NumericImputer missing_values NaN
    # NumericImputer strategy "constant
    # NumericImputer verbose 0
    numeric_imputer = impute.SimpleImputer(strategy='constant', fill_value=-1, missing_values=np.nan)
    # numeric_imputer = impute.SimpleImputer(strategy='constant', missing_values=np.nan)

    # StandardScaler copy true
    # StandardScaler with_mean true
    # StandardScaler with_std true
    numeric_scaler = preprocessing.StandardScaler(with_mean=True, with_std=True)

    numeric_transformer = replicator.make_numeric_transformer(numeric_imputer, numeric_scaler)

    # Imputer missing_values "NaN"
    # Imputer strategy "most_frequent"
    categorical_imputer = impute.SimpleImputer(strategy="most_frequent")

    # OneHotEncoder? categories null
    # OneHotEncoder? dtype {"oml-python:serialized_object": "type", "value": "np.float64
    # OneHotEncoder? handle_unknown "ignore
    # OneHotEncoder? sparse true
    categorical_encoder = preprocessing.OneHotEncoder(categories=None, dtype = np.float64, handle_unknown = "ignore", sparse=True)

    categorical_transfomer = replicator.make_categorical_transformer(categorical_imputer, categorical_encoder)
    preprocessor = replicator.make_preprocessing_step(features, numeric_transformer, categorical_transfomer)

    # Transform parameters
    # OneHotEncoder? n_jobs null
    # OneHotEncoder? remainder "passthrough
    # OneHotEncoder? sparse_threshold 0.3
    # OneHotEncoder? transformer_weights null

    # VarianceThreshold threshold 0.0
    selector = ("VOT", feature_selection.VarianceThreshold(threshold = 0.0))

    # SVC C 1.3038336700791593
    # SVC cache_size 200
    # SVC coef0 0.27655521693301055
    # SVC decision_function_shape "ovr
    # SVC degree 4
    # SVC gamma 0.9653942582600592
    # SVC kernel "poly
    # SVC max_iter -1
    # SVC probability false
    # SVC random_state 2614
    # SVC shrinking true
    # SVC tol 7.038926603676114e-05
    # SVC verbose false
    learner = ("SVC", svm.SVC(C = 1.3038336700791593, random_state=2614, cache_size = 200, kernel='poly', decision_function_shape = 'ovr', degree=4, gamma = 0.9653942582600592, coef0 = 0.27655521693301055, tol = 7.038926603676114e-05, shrinking = False))

    pipeline = pipelines.Pipeline(steps = [preprocessor, selector, learner])
    scorer = replicator.make_accuracy_scorer()

    scores = model_selection.cross_val_score(pipeline, x, y, scoring = scorer, cv=10)
    score = np.mean(scores)
    print("Score = ", score)

if __name__ == '__main__':
    run_replication()
