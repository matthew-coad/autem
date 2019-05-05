from autem import DataType, Role
from autem.evaluators import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, make_scorer
from sklearn.metrics import accuracy_score

import sklearn.pipeline
import sklearn.compose
import sklearn.preprocessing
import sklearn.impute
import sklearn.feature_selection
import sklearn.tree
import sklearn.svm


import openml

class BenchmarkScorer(Evaluater):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def evaluate_member(self, member):
        super().evaluate_member(member)

        settings = SimulationSettings(member)
        evaluation = member.evaluation
        random_state = settings.get_random_state()

        did = 470
        dataset = openml.datasets.get_dataset(did)

        x, y = dataset.get_data(target=dataset.default_target_attribute)
        pipeline = member.get_member_resources().pipeline
        scores = cross_val_score(pipeline, x, y, scoring = make_scorer(accuracy_score), cv=10)


        # We create the preprocessing pipelines for both numeric and categorical data.
        numeric_features = [0, 1, 2, 5, 6]
        numeric_imputer = sklearn.impute.SimpleImputer(strategy="mean")
        numeric_scaler = sklearn.preprocessing.data.StandardScaler(copy = True, with_mean=False, with_std=True)
        numeric_transformer = sklearn.pipeline.Pipeline(steps=[
            ('imputer', numeric_imputer),
            ('scaler', numeric_scaler)
        ])

        categorical_features = [3, 4, 7, 8]
        categorical_imputer = sklearn.impute.SimpleImputer(strategy="most_frequent")
        categorical_encoder = sklearn.preprocessing.data.OneHotEncoder(dtype = np.float64, handle_unknown = "ignore", sparse = True)
        categorical_transformer = sklearn.pipeline.Pipeline(steps=[
            ('imputer', categorical_imputer),
            ('encoder', categorical_encoder)
        ])

        preprocessor = sklearn.compose.ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])    

        imputer = sklearn.compose.ColumnTransformer(
            transformers=[
                ('num', numeric_imputer, numeric_features),
                ('cat', categorical_imputer, categorical_features)
            ])

        encoder = sklearn.compose.ColumnTransformer(
            transformers=[
                ('cat', categorical_encoder, categorical_features)
            ])    

        scaler = sklearn.compose.ColumnTransformer(
            transformers=[
                ('num', numeric_scaler, numeric_features)
            ])                

        pipeline2 = sklearn.pipeline.Pipeline(steps = 
        [
            ("ICN", imputer),
            ("EHO", encoder),
            ("SCL", scaler),

            (
                "VOT",
                sklearn.feature_selection.VarianceThreshold(threshold = 0.0)
            ),

            (
                "SVC",
                sklearn.svm.classes.SVC(
                    C = 734.2557240286019, cache_size = 200, class_weight = None, coef0 = 0.5834554995473993, decision_function_shape = None, degree = 2, 
                    gamma = 0.006910901548208322, kernel = "rbf", max_iter=-1,probability = True, random_state=39563, shrinking = False, tol = 1.6089614543017607e-05
                )
            )
        ])

        scores2 = cross_val_score(pipeline2, x, y, scoring = make_scorer(accuracy_score), cv=10)

        pipeline3 = sklearn.pipeline.Pipeline(steps = 
        [
            (
                "preprocess",
                preprocessor
            ),

            (
                "variencethreshold",
                sklearn.feature_selection.VarianceThreshold(threshold = 0.0)
            ),

            (
                "classifier",
                sklearn.svm.classes.SVC(
                    C = 734.2557240286019, cache_size = 200, class_weight = None, coef0 = 0.5834554995473993, decision_function_shape = None, degree = 2, 
                    gamma = 0.006910901548208322, kernel = "rbf", max_iter=-1,probability = True, random_state=39563, shrinking = False, tol = 1.6089614543017607e-05
                )
            )
        ])

        scores3 = cross_val_score(pipeline3, x, y, scoring = make_scorer(accuracy_score), cv=10)

        evaluation.scores = scores2

