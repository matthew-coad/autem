from .group import Group
from .dataset import Dataset
from .role import Role

from types import SimpleNamespace

class Component:

    def __init__(self, name, group_name = None, parameters = []):
        self.name = name
        self.group_name = group_name
        self.parameters = parameters

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        if not self.group_name is None and not outline.has_attribute(self.group_name, Dataset.Battle):
            outline.append_attribute(self.group_name, Dataset.Battle, [ Role.Measure ], self.group_name)
        for parameter in self.parameters:
            parameter.outline_simulation(self, simulation, outline)

    def start_simulation(self, simulation):
        """
        Start a simulation
        """
        for parameter in self.parameters:
            parameter.start_simulation(self, simulation)

    def get_group(self, member):
        if self.group_name is None:
            return None
        return getattr(member.configuration, self.group_name)

    def start_group(self, member):
        """
        Perform member startup for a component group
        """
        if not hasattr(member.configuration, self.group_name):
            setattr(member.configuration, self.group_name, Group())
        group = self.get_group(member)
        group.components.append(self.name)
        # On start select one component to be the active one
        random_state = member.simulation.random_state
        component_index = len(group.components) - 1
        if component_index > 0:
            replace = random_state.randint(0, len(group.components)) == 0
            if replace:
                delattr(member.configuration, group.active)
                group.active = group.components[component_index]
        else:
            group.active = group.components[component_index]

    def is_active(self, member):
        """
        Is this component active for the selected member?
        """
        if self.group_name is None:
            # Components that aren't grouped are always active
            return True
        group = self.get_group(member)
        return group.active == self.name

    def get_active_name(self, member):
        """
        Get the name of the component that is active
        """
        if self.group_name is None:
            # If the component isn't grouped then its the active one!
            return self.name
        group = self.get_group(member)
        return group.active

    def start_member(self, member):
        """
        Start a member
        """
        if not self.group_name is None:
            self.start_group(member)
        if self.is_active(member):
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.start_member(self, member)

    def copy_group(self, member, prior):
        """
        Copy group configuration
        """
        if hasattr(member.configuration, self.group_name):
            return None
        prior_group = getattr(prior.configuration, self.group_name)
        group = Group()
        group.components = prior_group.components[:]
        group.active = prior_group.active
        setattr(member.configuration, self.group_name, group)

    def copy_member(self, member, prior):
        """
        Start a member
        """
        if not self.group_name is None:
            self.copy_group(member, prior)
        if self.is_active(member):
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.copy_member(self, member, prior)

    def mutate_member(self, member):
        """
        Mutate a member
        """
        if not self.is_active(member):
            return False
        random_state = member.simulation.random_state
        parameters = self.parameters
        n_parameters = len(parameters)
        if not n_parameters:
            return False

        parameter_indexes = random_state.choice(n_parameters, size=n_parameters, replace=False)
        for parameter_index in parameter_indexes:
            parameter = parameters[parameter_index]
            mutated = parameter.mutate_member(self, member)
            if mutated:
                return True
        return False

    def crossover_member(self, member, parent0, parent1):
        random_state = member.simulation.random_state

        # If we are in group mode and this is the first group
        # pick one of the parents to base my group and vcopy it
        if not self.group_name is None and not hasattr(member.configuration, self.group_name):
            parent0_group = self.get_group(parent0)
            parent1_group = self.get_group(parent1)
            parent_index = random_state.randint(0,2)
            parent_group = parent0_group if parent_index == 0 else parent1_group
            group = Group()
            group.active = parent_group.active
            group.components = parent_group.components[:]
            setattr(member.configuration, self.group_name, group)
        else:
            group = self.get_group(member)

        if not group is None and group.active == self.name:
            # We are crossing over the selected component in group mode
            setattr(member.configuration, self.name, SimpleNamespace())
            parent0_group = self.get_group(parent0)
            parent1_group = self.get_group(parent1)
            if parent0_group.active == parent1_group.active:
                # Parents have the same component
                # Do a parameter wise copy
                for parameter in self.parameters:
                    parameter.crossover_member(self, member, parent0, parent1)
            else:
                # Parents don't match
                # Do a copy of the selected parent
                parent = parent0 if parent0_group.active == group.active else parent1
                for parameter in self.parameters:
                    parameter.copy_member(self, member, parent)
        elif group is None:
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.crossover_member(self, member, parent0, parent1)

    def evaluate_member(self, member, evaluation):
        """
        Perform a round of member evaluation
        """
        pass

    def contest_members(self, member1, member2, outcome):
        """
        Run a battle between two members
        """
        pass

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        if not self.is_active(member):
            return False
        if not self.group_name is None:
            group = self.get_group(member)
            setattr(record, self.group_name, group.active)
        for parameter in self.parameters:
            parameter.record_member(self, member, record)

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        pass

