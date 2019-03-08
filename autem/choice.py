from .dataset import Dataset
from .role import Role

from .hyper_parameter import HyperParameter

class Choice(HyperParameter):

    """
    Defines a set of components where only one component can be active for a member
    Groups can only act as hyper parameters
    """
    def __init__(self, choice_name = None, components = []):
        HyperParameter.__init__(self, choice_name)
        self.components = components
        for component in components:
            if component.is_hyper_parameter():
                component.set_choice_name(choice_name)

    def set_group_name(group_name):
        raise RuntimeError("Cannot change group name of a choice")

    def set_choice_name(choice_name):
        raise RuntimeError("Cannot change choice name of a choice")

    # Outline

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        outline.append_attribute(self.name, Dataset.Battle, [ Role.Parameter ], self.name)
        for component in self.components:
            component.outline_simulation(simulation, outline)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        setattr(record, self.name, self.get_active_component_name(member))
        component = self.get_active_component(member)
        component.record_member(member, record)

    # Active component

    def get_component_names(self):
        """
        Get all component names
        """
        component_names = [ c.name for c in self.components ]
        return component_names

    def get_active_component_name(self, member):
        """
        Get the name of the component that is active for the member
        """
        active_name = getattr(member.configuration, self.name)
        return active_name

    def set_active_component_name(self, member, component_name):
        """
        Set the name of the component that is active for the member
        """
        setattr(member.configuration, self.name, component_name)

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

    def copy_member(self, member, prior):
        """
        Copy the component configuration
        """
        component_name = self.get_active_component_name(prior)
        self.set_active_component_name(member, component_name)
        self.get_active_component(member).copy_member(member, prior)

    def force_member(self, member, component_name):
        """
        Initialize a member forced to take on a specific value
        """
        prior_active_component = self.get_active_component_name(member)
        if prior_active_component != component_name:
            if hasattr(member.configuration, prior_active_component):
                delattr(member.configuration, prior_active_component)
            self.set_active_component_name(member, component_name)
            self.get_active_component(member).initialize_member(member)

    # Mutation

    def mutate_member(self, member):
        """
        Forward mutation to the selected component
        """
        return self.get_active_component(member).mutate_member(member)

    def transmute_member(self, member):
        """
        Perform a major change to the member
        """
        random_state = member.simulation.random_state
        current_active_component_name = self.get_active_component_name(member)
        components = self.components
        if len(components) < 2:
            return False

        attempts = 0
        max_attempts = 50
        mutated = False
        component_name = None
        while component_name is None:
            component_index = random_state.randint(0, len(components))
            if components[component_index].name != current_active_component_name:
                component_name = components[component_index].name
            else:
                # We expect things to mutate quickly
                # But make sure we don't get stuck in an infinite loop
                attempts += 1
                if attempts > max_attempts:
                    raise RuntimeError("Attempt to transmute choice failed")
        self.force_member(member, component_name)
        return True

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



