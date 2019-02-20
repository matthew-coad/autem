from .parameter import Parameter

class ChoicesParameter(Parameter):

    def __init__(self, name, label, choices, first_choice):
        Parameter.__init__(self, name, label)
        self.label = label
        self.first_choice = first_choice
        self.choices = choices
        if len(choices) < 2:
            raise RuntimeError("At least 2 choices required")

    def get_initial_value(self, member):
        return self.first_choice

    def get_mutated_value(self, member):
        random_state = member.simulation.random_state
        choice_index = random_state.randint(0, len(self.choices))
        return self.choices[choice_index]
