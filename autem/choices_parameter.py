from .parameter import Parameter

class ChoicesParameter(Parameter):

    def __init__(self, name, label, choices, shared = False):
        Parameter.__init__(self, name, label, shared)
        self.choices = choices
        if len(choices) < 2:
            raise RuntimeError("At least 2 choices required")

    def get_initial_value(self, member):
        return None

    def get_mutated_value(self, member):
        random_state = member.get_random_state()
        choice_index = random_state.randint(0, len(self.choices))
        return self.choices[choice_index]

def make_choice(name, choices):
    return ChoicesParameter(name, name, choices)

def make_choice_list(choice_dict):
    """
    Make a set of choice parameters from a dictionary of name, choices dictionary
    """
    parameters = [ make_choice(k, choice_dict[k]) for k in choice_dict]
    return parameters
