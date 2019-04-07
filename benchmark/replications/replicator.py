import numpy as np
from scipy import stats

import sklearn.base as base
import sklearn.impute as impute
import sklearn.preprocessing as preprocessing
import sklearn.pipeline as pipeline
import sklearn.compose as compose
import sklearn.model_selection as model_selection
import sklearn.metrics as metrics

import openml

def get_dataset(did):
    dataset = openml.datasets.get_dataset(did)
    return dataset

def get_data(dataset):
    x, y = dataset.get_data(target=dataset.default_target_attribute)
    return (x, y)

def get_features(dataset):
    feature_exclude = [ dataset.default_target_attribute ]
    nominal_features = dataset.get_features_by_type("nominal", exclude=feature_exclude)
    numeric_features = dataset.get_features_by_type("numeric", exclude=feature_exclude)
    date_features = dataset.get_features_by_type("date", exclude=feature_exclude)
    string_features = dataset.get_features_by_type("string", exclude=feature_exclude)
    features = {
        "nominal": nominal_features,
        "numeric": numeric_features,
        "date": date_features,
        "string": string_features
    }
    return features

def make_numeric_transformer(numeric_imputer, numeric_scaler):
    # We create the preprocessing pipelines for both numeric and categorical data.
    # numeric_features = [0, 1, 2, 5, 6]
    numeric_transformer = pipeline.Pipeline(steps=[
        ('imp', numeric_imputer),
        ('scaler', numeric_scaler)
    ])
    return numeric_transformer

def get_one_hot_categories(x, features):
    categorical_features = features['nominal']
    categories = []
    for feature in categorical_features:
        values = np.unique(x[:,feature])
        values = values[~np.isnan(values)]
        values = np.sort(values)
        categories.append(values)
    return categories

def make_categorical_transformer(categorical_imputer, categorical_encoder):
    categorical_transformer = pipeline.Pipeline(steps=[
        ('imp', categorical_imputer),
        ('enc', categorical_encoder)
    ])
    return categorical_transformer

def make_preprocessing_step(features, numeric_transformer, categorical_transformer):

    nominal_features = features["nominal"]
    numeric_features = features["numeric"]

    step = (
        "PREP", 
        compose.ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, nominal_features)]
        )
    )
    return step

def make_accuracy_scorer():
    return metrics.make_scorer(metrics.accuracy_score)

def score_pipeline(x, y, pipeline, scorer):
    scores = model_selection.cross_val_score(pipeline, x, y, scoring = scorer, cv=10)
    score = np.mean(scores)
    return score

