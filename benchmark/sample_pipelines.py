


pipesklearn.pipeline.Pipeline(
    columntransformer=sklearn.compose._column_transformer.ColumnTransformer(
    numeric=sklearn.pipeline.Pipeline(
        imputer=sklearn.preprocessing.imputation.Imputer, 
        standardscaler=sklearn.preprocessing.data.StandardScaler
        ),
        nominal=sklearn.pipeline.Pipeline(
            simpleimputer=sklearn.impute.SimpleImputer,
            onehotencoder=sklearn.preprocessing._encoders.OneHotEncoder)
    ),
    variancethreshold=sklearn.feature_selection.variance_threshold.VarianceThreshold,
    svc=sklearn.svm.classes.SVC
)
