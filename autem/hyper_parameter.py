class HyperParameter:

    def __init__(self, name):
        self._name = name
        self._group_name = None
        self._choice_name = None

    # Properties

    ## Name

    def get_name(self):
        return self._name

    ## Group name

    def get_group_name(self):
        return self._group_name

    def set_group_name(self, group_name):
        self._group_name = group_name

    ## Choice name

    def get_choice_name(self):
        return self._choice_name

    def set_choice_name(self, choice_name):
        self._choice_name = choice_name

    # Workflow

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

class HyperParameterContainer:

    def list_hyper_parameters(self):
        hyper_parameters = [c for c in self.list_components() if isinstance(c, HyperParameter) ]
        return hyper_parameters

