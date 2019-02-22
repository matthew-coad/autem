from .dataset import Dataset
from .role import Role
from .hyper_parameter import HyperParameter

from types import SimpleNamespace

class Group(HyperParameter):

    """
    Defines a group of hyper parameters
    """
    def __init__(self, name, parameters, preference = 0):
        HyperParameter.__init__(self, name)
        self.parameters = parameters
        self.preference = preference
        for parameter in parameters:
            parameter.group_name = self.name

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        for parameter in self.parameters:
            parameter.outline_simulation(simulation, outline)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        for parameter in self.parameters:
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

        random_state = member.simulation.random_state
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
            random_state = member.simulation.random_state
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.crossover_member(member, parent0, parent1)

