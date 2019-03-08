from .component import Component

class HyperParameter(Component):

    def __init__(self, name):
        self.name = name

    def is_hyper_parameter(self):
        """
        Is this component a hyper parameter for the simulation
        """
        return True

    def is_controller(self):
        """
        Is this component responsible for controlling the simulation
        """
        return False

    def set_group_name(self, choice_name):
        raise NotImplementedError()

    def set_choice_name(self, choice_name):
        raise NotImplementedError()

    def initialize_member(self, member):
        """
        Initialize a member
        """
        raise NotImplementedError()

    def copy_member(self, member, prior):
        """
        Copy the component configuration
        """
        raise NotImplementedError()

    def mutate_member(self, member):
        """
        Mutate a member
        """
        raise NotImplementedError()

    def transmute_member(self, member):
        """
        Transmute a member
        """
        # Forward to mutate by default
        return self.mutate_member(member)

    def crossover_member(self, member, parent0, parent1):
        raise NotImplementedError()

    def prepare_member(self, member):
        """
        Perform member for running
        """
        pass

