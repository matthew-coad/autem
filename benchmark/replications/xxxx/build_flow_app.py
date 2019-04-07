if __name__ == '__main__':
    import context

import openml
import sklearn.pipeline
import sklearn.compose
import sklearn.preprocessing
import sklearn.impute
import sklearn.feature_selection
import sklearn.tree
import sklearn.svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, make_scorer
import benchmark.utility as utility
import pandas as pd
import numpy as np
import json
from pprint import pprint

utility.prepare_OpenML()

class ComponentReference:

    def __init__(self, key, step_name, argument_1 = None):
        self.key = key
        self.step_name = step_name
        self.argument_1 = argument_1

class BaseConverter:

    def __init__(self, class_name, factory = None):
        self.class_name = class_name

    def convert(self, component):
        raise NotImplementedError()

    def convert_parameter(self, component, key, parameter):
        return parameter

    def convert_parameters(self, component):
        converts = {}
        parameters = component.parameters
        for key in parameters:
            parameter = parameters[key]
            converted = self.convert_parameter(component, key, parameter)
            if not converted is None:
                converts[key] = converted
        return converts        

    def convert_children(self, component):
        converts = {}
        for key in component.components:
            child = component.components[key]
            child_converter = converter_lookup[child.class_name]
            converts[key] = child_converter.convert(child)
        return converts

class SimpleConverter(BaseConverter):

    def __init__(self, class_name, factory):
        BaseConverter.__init__(self, class_name)
        self.factory = factory

    def convert(self, component):
        factory = self.factory
        converted = factory()
        parameters = self.convert_parameters(component)
        converted.set_params(**parameters)
        return converted

class PipelineConverter(BaseConverter):

    def __init__(self):
        BaseConverter.__init__(self, 'sklearn.pipeline.Pipeline')

    def convert_step_reference(self, component, item):
        value = item["value"]
        key = value["key"]
        step_name = value["step_name"]
        reference = ComponentReference(key, step_name)
        return reference

    def convert_step_references(self, component):
        steps_text = component.parameters['steps']
        steps_object = json.loads(steps_text)
        step_references = [ self.convert_step_reference(component, si) for si in steps_object]
        return step_references

    def convert_steps(self, component):
        step_references = self.convert_step_references(component)
        children = self.convert_children(component)
        steps = []
        for ref in step_references:
            key = ref.key
            step_name = ref.step_name
            step = children[key]
            steps.append((step_name, step))
        return steps

    def convert(self, component):
        steps = self.convert_steps(component)
        memory = component.parameters["memory"]
        pipeline = sklearn.pipeline.Pipeline(steps = steps, memory = memory)
        return pipeline

class ColumnTransformerConverter(BaseConverter):        

    def __init__(self):
        BaseConverter.__init__(self, 'sklearn.compose._column_transformer.ColumnTransformer')

    def convert_transformer_reference(self, component, item):
        value = item["value"]
        key = value["key"]
        step_name = value["step_name"]
        argument_1 = value["argument_1"]
        reference = ComponentReference(key, step_name, argument_1)
        return reference

    def convert_transformer_references(self, component):
        text = component.parameters['transformers']
        transformers_object = json.loads(text)
        references = [ self.convert_transformer_reference(component, si) for si in transformers_object]
        return references

    def convert_transformers(self, component):
        references = self.convert_transformer_references(component)
        children = self.convert_children(component)
        transformers = []
        for ref in references:
            key = ref.key
            step_name = ref.step_name
            columns = ref.argument_1
            transformer = children[key]
            transformers.append((step_name,  transformer, columns ))
        return transformers

    def convert(self, component):
        transformers = self.convert_transformers(component)
        transformer = sklearn.compose.ColumnTransformer(transformers)
        return transformer

class ImputerConverter(SimpleConverter):

    def __init__(self):
        SimpleConverter.__init__(self, 'sklearn.preprocessing.imputation.Imputer', lambda: sklearn.impute.SimpleImputer())

    def convert_parameters(self, component):
        parameters = super().convert_parameters(component)
        if 'axis' in parameters:
            del parameters['axis']
        return parameters

converters = [
    PipelineConverter(),
    ColumnTransformerConverter(),
    ImputerConverter(),
    SimpleConverter('sklearn.preprocessing.data.StandardScaler', lambda: sklearn.preprocessing.StandardScaler()),
    SimpleConverter('sklearn.preprocessing._encoders.OneHotEncoder', lambda: sklearn.preprocessing.OneHotEncoder()),

    SimpleConverter('sklearn.feature_selection.variance_threshold.VarianceThreshold', lambda: sklearn.feature_selection.VarianceThreshold()),

    SimpleConverter('sklearn.impute.SimpleImputer', lambda: sklearn.impute.SimpleImputer()),

    SimpleConverter('sklearn.svm.classes.SVC', lambda: sklearn.svm.SVC()),
]

converter_lookup = dict([ (c.class_name, c) for c in converters ])

def convert_component(component):
    converter = converter_lookup[component.class_name]
    converted = converter.convert(component)
    return converted



task_id = 3561
# flow = openml.flows.get_flow(8817)
# pipeline = convert_component(flow)
# task = openml.tasks.get_task(task_id)

did = 470
dataset = openml.datasets.get_dataset(did)

categorical = dataset.get_data(return_categorical_indicator=True)
categorical = categorical[:-1]  # Remove last index (which is the class)

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

pipeline = sklearn.pipeline.Pipeline(steps = 
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

x, y = dataset.get_data(target=dataset.default_target_attribute)
scores = cross_val_score(pipeline, x, y, scoring = make_scorer(accuracy_score), cv=10)
pprint(scores)


#task_id = 3561
#task = openml.tasks.get_task(task_id)
#run = openml.runs.run_model_on_task(task, conditional_pipe2)
#predictive_accuracy = run.fold_evaluations['predictive_accuracy']
#scores = np.array([score for rep, folds in predictive_accuracy.items() for fold, score in folds.items()])
#pprint(scores)


#validation_size = 0.2
#x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size)
#hand_pipe2.fit(x_train, y_train)
#y_pred = hand_pipe2.predict(x_validation)

#score = accuracy_score(y_validation, y_pred)
#print(score)

# run = openml.runs.run_model_on_task(task, pipeline)
# predictive_accuracy = run.fold_evaluations['predictive_accuracy']
#scores = np.array([score for rep, folds in predictive_accuracy.items() for fold, score in folds.items()])
#pprint(scores)

#rep = repr(c)
#pprint(convert_component(flow))

#onehotencoder = sklearn.preprocessing.OneHotEncoder()
#nominal = sklearn.pipeline.Pipeline()
#transformer = sklearn.compose.ColumnTransformer()

#pipeline = sklearn.pipeline.Pipeline()