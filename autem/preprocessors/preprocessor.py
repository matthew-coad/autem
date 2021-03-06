from ..group import Group
from ..reporters import DataType, Role
from ..choices_parameter import ChoicesParameter, make_choice, make_choice_list

import numpy as np

class Preprocesssor(Group):

    def __init__(self, name, label, parameters):
        Group.__init__(self, name, parameters)
        self.label = label

    def make_preprocessor(self, member):
        raise NotImplementedError()

    def configure_preprocessor(self, member, pre_processor):
        pre_processor_params = pre_processor.get_params().keys()
        params = {}
        if len(self.parameters) > 0:
            pairs = [(p.get_name(), p.get_value(member)) for p in self.parameters]
            params = dict(p for p in pairs if not p[1] is None)
            pre_processor.set_params(**params)

    def read_preprocessor(self, member, pre_processor):
        """
        Read the configuration back from the preprocessor
        returns a dict of parameter name value pairs
        """
        params = pre_processor.get_params()
        result = {}
        parameter_names = [ p.get_name() for p in self.parameters ]
        for key in parameter_names:
            value = params[key]
            result[key] = value
        return result

    def update_parameters(self, member, pre_processor):
        """
        Update the parameters so they match the configured values
        """
        values = self.read_preprocessor(member, pre_processor)
        for key in values:
            parameter = self.get_parameter(key)
            parameter.set_value(member, values[key])

    def prepare_member(self, member):
        super().prepare_member(member)

        processor_name = self.get_name()
        preprocessor = self.make_preprocessor(member)
        if preprocessor is None:
            return None

        self.configure_preprocessor(member, preprocessor)
        self.update_parameters(member, preprocessor)

        steps = member.get_steps()
        steps.append((processor_name, preprocessor))

class PreprocessorContainer:

    def get_steps(self):
        steps = self.get_state("steps", lambda: [])
        return steps

