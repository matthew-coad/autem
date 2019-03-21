import sklearn
import openml

import sklearn.base
import sklearn.impute as impute
import sklearn.preprocessing as preprocessing
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 
from sklearn.model_selection import train_test_split
import sklearn.feature_selection as feature_selection
import sklearn.decomposition as decomposition
import sklearn.kernel_approximation as kernel_approximation
import sklearn.tree as tree

import numpy as np
import time

did = 24
dataset = openml.datasets.get_dataset(did)
x, y = dataset.get_data(target=dataset.default_target_attribute)
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
categorical_features = nominal_features
validation_size = 0.2
seed = 1234
random_state = np.random.RandomState(seed)

x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, random_state=random_state)
x_pipe = x_train
y_pipe = y_train

#Scaler	Scaler_num__imp__strategy,	Selector	LVT_threshold	Reducer	PCA_iterated_power	
#YJH,	median,	                    LVT,	    0,	            PCA,	auto,	            

#Approximator	NYS_kernel	NYS_gamma	NYS_n_components	Learner	CART_criterion	CART_max_depth	CART_min_samples_split	CART_min_samples_leaf
#NYS,	        rbf,		100,	                        CART,	entropy,		                2,	                    1

# YJH	median	LVT	0	PCA	auto	NYS	rbf		100	CART	entropy		2	1													

categories = []
for feature in categorical_features:
    values = np.unique(x[:,feature])
    values = values[~np.isnan(values)]
    values = np.sort(values)
    categories.append(values)

#Scaler	Scaler_num__imp__strategy,	
#YJH,	median,	                    


# We create the preprocessing pipelines for both numeric and categorical data.
# numeric_features = [0, 1, 2, 5, 6]
numeric_imputer = impute.SimpleImputer(strategy='median')
numeric_scaler = preprocessing.PowerTransformer(method = "yeo-johnson", standardize=True)

numeric_transformer = Pipeline(steps=[
    ('imp', numeric_imputer),
    ('scaler', numeric_scaler)
])

# categorical_features = [3, 4, 7, 8]
categorical_imputer = impute.SimpleImputer(strategy="most_frequent")
categorical_encoder = preprocessing.OneHotEncoder(categories=categories, dtype = np.float64, handle_unknown = "error", sparse=False)
categorical_transformer = Pipeline(steps=[
    ('imp', categorical_imputer),
    ('enc', categorical_encoder)
])

start = time.time()
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

preprocessor.set_params(num__imp__strategy = 'median')

for i in range(10):
    sklearn.base.clone(preprocessor).fit(x_pipe, y_pipe)

end = time.time()
duration = end - start
print("scale", duration)
# .4 Of a second to scale

preprocessor.fit_transform(x_pipe, y_pipe)
x_pipe = preprocessor.transform(x_pipe)

#Selector	LVT_threshold	Reducer	PCA_iterated_power	
#LVT,	    0,	            PCA,	auto,	            

selector = feature_selection.VarianceThreshold()
selector.set_params(threshold = 0)

start = time.time()

for i in range(10):
    sklearn.base.clone(selector).fit_transform(x_pipe, y_pipe)

end = time.time()
duration = end - start
print("selector", duration)

# .008 seconds to select

selector.fit(x_pipe, y_pipe)
x_pipe = selector.transform(x_pipe)

#Reducer	PCA_iterated_power
#PCA,	auto,
 
reducer = decomposition.PCA(svd_solver = 'randomized')
reducer.set_params(iterated_power = 'auto')

start = time.time()

for i in range(10):
    sklearn.base.clone(reducer).fit_transform(x_pipe, y_pipe)

end = time.time()
duration = end - start
print("reducer", duration)

# 2

reducer.fit(x_pipe, y_pipe)
x_pipe = reducer.transform(x_pipe)

#Approximator	NYS_kernel	NYS_gamma	NYS_n_components
#NYS,	        rbf,		100,	                    

approximator = kernel_approximation.Nystroem()
approximator.set_params(kernel = 'rbf', gamma = None, n_components = 100)

start = time.time()
for i in range(10):
    sklearn.base.clone(approximator).fit_transform(x_pipe, y_pipe)

end = time.time()
duration = end - start
print("approximator", duration)

# .24
approximator.fit(x_pipe, y_pipe)
x_pipe = approximator.transform(x_pipe)


#Approximator	NYS_kernel	NYS_gamma	NYS_n_components	Learner	CART_criterion	CART_max_depth	CART_min_samples_split	CART_min_samples_leaf
#NYS,	        rbf,		100,	                        CART,	entropy,		                2,	                    1


learner = tree.DecisionTreeClassifier()
learner.set_params(criterion = 'entropy', max_depth = None, min_samples_split = 2, min_samples_leaf = 1)

start = time.time()
for i in range(10):
    sklearn.base.clone(learner).fit(x_pipe, y_pipe)

end = time.time()
duration = end - start
print("learner", duration)
