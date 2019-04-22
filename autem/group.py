from .reporting import Dataset, Role, Reporter
from .hyper_parameter import HyperParameter
from .lifecycle import LifecycleManager

from types import SimpleNamespace

class Group(HyperParameter, LifecycleManager, Reporter):

    """
    Defines a group of hyper parameters
    """
    def __init__(self, group_name, parameters):
        HyperParameter.__init__(self, group_name)
        LifecycleManager.__init__(self)
        self.parameters = parameters
        for parameter in parameters:
            parameter.set_group_name(group_name)

    def set_group_name(self, group_name):
        raise RuntimeError("Cannot change name of a group")

    def set_choice_name(self, choice_name):
        self.choice_name = choice_name
        for parameter in self.parameters:
            parameter.set_choice_name(choice_name)

    def get_parameter(self, name):
        params = [p for p in self.parameters if p.name == name ]
        if len(params) != 1:
            raise RuntimeError("Parameter not found")
        return params[0]

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        for parameter in self.parameters:
            if isinstance(parameter, Reporter):
                parameter.outline_simulation(simulation, outline)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        for parameter in self.parameters:
            if isinstance(parameter, Reporter):
                parameter.record_member(member, record)

    def initialize_member(self, member):
        """
        Initialize a member
        """
        if self.parameters:
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.initialize_member(member)

    def copy_member(self, member, prior):
        """
        Copy the component configuration
        """
        if self.parameters:
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.copy_member(member, prior)

    def mutate_member(self, member):
        """
        Mutate a member
        """
        if not self.parameters:
            return False

        random_state = member.get_random_state()
        parameters = self.parameters

        n_parameters = len(parameters)
        parameter_indexes = random_state.choice(n_parameters, size=n_parameters, replace=False)
        for parameter_index in parameter_indexes:
            parameter = parameters[parameter_index]
            mutated = parameter.mutate_member(member)
            if mutated:
                return True
        return False

    def crossover_member(self, member, parent0, parent1):
        if self.parameters:
            random_state = member.get_random_state()
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.crossover_member(member, parent0, parent1)

    def prepare_member(self, member):
        for parameter in self.parameters:
            if isinstance(parameter, LifecycleManager):
                parameter.prepare_member(member)

    def bury_member(self, member):
        for parameter in self.parameters:
            if isinstance(parameter, LifecycleManager):
                parameter.bury_member(member)
