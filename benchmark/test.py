import sklearn
import sklearn.svm

sklearn.svm.SVC(C = 143.0, coef0 = 0.229, degree = 2, gamma = 0.0007, kernel = 'poly', tol = 1.1571247532842242e-05     )) )

import openml

run = openml.runs.get_run(8837993)
model = openml.runs.initialize_model_from_run(8837993)

sklearn.pipeline.Pipeline(
    columntransformer = sklearn.compose._column_transformer.ColumnTransformer(
        numeric= sklearn.pipeline.Pipeline(
            imputer=sklearn.preprocessing.imputation.Imputer,
            standardscaler=sklearn.preprocessing.data.StandardScaler),
        nominal=sklearn.pipeline.Pipeline(
            simpleimputer=sklearn.impute.SimpleImputer,
            onehotencoder=sklearn.preprocessing._encoders.OneHotEncoder)
        ),
        variancethreshold=sklearn.feature_selection.variance_threshold.VarianceThreshold,
        svc=sklearn.svm.SVC(C = 143.0, coef0 = 0.229, degree = 2, gamma = 0.0007, kernel = 'poly', tol = 1.1571247532842242e-05     )) )
