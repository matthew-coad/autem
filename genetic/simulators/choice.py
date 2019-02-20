from .dataset import Dataset
from .role import Role

from .hyper_parameter import HyperParameter

class Choice(HyperParameter):

    """
    Defines a set of components where only one component can be active for a member
    Groups can only act as hyper parameters
    """
    def __init__(self, group_name = None, components = []):
        HyperParameter.__init__(self, group_name)
        self.group_name = group_name
        self.components = components

    # Outline

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        outline.append_attribute(self.group_name, Dataset.Battle, [ Role.Parameter ], self.group_name)
        for component in self.components:
            component.outline_simulation(simulation, outline)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        setattr(record, self.group_name, self.get_active_component_name(member))
        self.get_active_component(member).record_member(member, record)

    # Active component

    def get_active_component_name(self, member):
        """
        Get the name of the component that is active for the member
        """
        active_name = getattr(member.configuration, self.group_name)
        return active_name

    def set_active_component_name(self, member, component_name):
        """
        Set the name of the component that is active for the member
        """
        setattr(member.configuration, self.group_name, component_name)

    def get_active_component(self, member):
        component_name = self.get_active_component_name(member)
        candidates = [c for c in self.components if c.name == component_name]
        if len(candidates) != 1:
            raise RuntimeError("Cannot find active component")
        return candidates[0]

    # Initialize

    def initialize_member(self, member):
        """
        To start a member set a component as active and start it
        """
        components = self.components
        random_state = member.simulation.random_state
        component_index = random_state.randint(0, len(components))
        component = components[component_index]
        self.set_active_component_name(member, component.name)
        component.initialize_member(member)

    # Mutation

    def mutate_member(self, member):
        """
        To mutate a member simply forward the request to the active component
        """
        return self.get_active_component(member).mutate_member(member)

    # Cross over

    def crossover_member(self, member, parent0, parent1):
        """
        Cross over members 
        """
        random_state = member.simulation.random_state

        # If we are in group mode and this is the first group
        # pick one of the parents to base my group on
        parent_index = random_state.randint(0,2)
        parent = parent0 if parent_index == 0 else parent1
        parent_name = self.get_active_component_name(parent)
        self.set_active_component_name(member, parent_name)
        active_component = self.get_active_component(member)

        parent0_name = self.get_active_component_name(parent0)
        parent1_name = self.get_active_component_name(parent1)

        if parent0_name == parent1_name:
            # Both parents share the active component
            # Forward the cross over request to the active component
            active_component.crossover_member(member, parent0, parent1)
        else:
            # Parents don't match
            # Do a copy of the selected parent
            active_component.copy_member(member, parent)

    # Lifecycle

    def prepare_member(self, member):
        """
        Forward request to active component
        """
        return self.get_active_component(member).prepare_member(member)



