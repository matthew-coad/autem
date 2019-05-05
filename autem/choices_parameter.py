from .parameter import Parameter

import numpy as np

class ChoicesParameter(Parameter):

    def __init__(self, name, label, feature_type, choices, shared = False):
        Parameter.__init__(self, name, label, feature_type, shared)
        self.choices = choices if not type(choices) is np.ndarray else choices.tolist()
        if len(choices) < 2:
            raise RuntimeError("At least 2 choices required")

    def get_initial_value(self, member):
        return None

    def get_mutated_value(self, member):
        random_state = SimulationSettings(member).get_random_state()
        choice_index = random_state.randint(0, len(self.choices))
        return self.choices[choice_index]

def make_choice(name, type, choices):
    return ChoicesParameter(name, name, type, choices)

def make_choice_list(choice_dict):
    """
    Make a set of choice parameters from a dictionary of name, choices dictionary
    """
    def make_type_choice_list(type):
        if not type in ['numeric', 'nominal']:
            raise RuntimeError("Invalid choice type")
        if not type in choice_dict:
            return []
        return [ make_choice(k, type, choice_dict[type][k]) for k in choice_dict[type]]
    choice_list = []
    for key in choice_dict:
        choice_list = choice_list + make_type_choice_list(key)
    return choice_list
