from .parameter import Parameter

class ChoicesParameter(Parameter):

    def __init__(self, name, role, label, choices, first_choice):
        self.name = name
        self.role = role
        self.label = label
        self.first_choice = first_choice
        self.choices = choices
        if len(choices) < 2:
            raise RuntimeError("At least 2 choices required")

    def get_start_value(self, component, member):
        # Select first choice if given
        if not self.first_choice is None :
            return self.first_choice
        # Otherwise select a choice at random
        random_state = member.simulation.random_state
        choice_index = random_state.randint(0, len(self.choices))
        return self.choices[choice_index]

    def get_mutated_value(self, component, member):
        random_state = member.simulation.random_state
        choice_index = random_state.randint(0, len(self.choices))
        return self.choices[choice_index]
