class HyperParameter:

    def __init__(self, name):
        self.name = name

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

class HyperParameterContainer:

    def list_hyper_parameters(self):
        hyper_parameters = [c for c in self.list_components() if isinstance(c, HyperParameter) ]
        return hyper_parameters

