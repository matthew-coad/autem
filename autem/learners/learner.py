from ..parameter import Parameter
from ..group import Group
from ..reporters import DataType, Role

from types import SimpleNamespace

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import numpy as np
from scipy import stats

import time

class Learner(Group):

    def __init__(self, name, label, parameters):
        Group.__init__(self, name, parameters)
        self.label = label

    def make_model(self):
        raise NotImplementedError()

    def read_params(self, member, pre_processor):
        """
        Read the configuration back from the preprocessor
        returns a dict of parameter name value pairs
        """
        params = pre_processor.get_params()
        result = {}
        parameter_names = [ p.name for p in self.parameters ]
        for key in params.keys():
            value = params[key]
            if key in parameter_names and not value is None:
                result[key] = value
        return result

    def update_parameters(self, member, pre_processor):
        """
        Update the parameters so they match the configured values
        """
        values = self.read_params(member, member, pre_processor)
        for key in values:
            parameter = self.get_parameter(key)
            parameter.set_value(member, values[key])


    def prepare_member(self, member):
        learner_name = self.name

        # Initialize the model parameters
        model = self.make_model()
        model_params = model.get_params().keys()
        learner_name = self.name
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.name, p.get_value(member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
        if 'n_jobs' in model_params:
            params['n_jobs'] = member.get_simulation().get_n_jobs()
        model.set_params(**params)

        # Read the final model parameters 
        final_params = model.get_params()
        for parameter in self.parameters:
            if parameter.name in final_params:
                value = final_params[parameter.name]
                parameter.set_value(member, value)

        # Build the pipeline
        steps = member.get_steps()
        steps.append((learner_name, model))
        memory = member.get_simulation().get_memory()
        pipeline = Pipeline(steps=steps, memory=memory)
        member.set_state("pipeline", pipeline)

    def bury_member(self, member):
        member.set_state("pipeline", None)
        member.set_state("steps", None)

class LearnerContainer:

    def get_pipeline(self):
        return self.get_state("pipeline")
