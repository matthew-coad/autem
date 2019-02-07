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
        if self.group_name and not outline.has_attribute(self.group_name, Dataset.Battle):
            outline.append_attribute(self.group_name, Dataset.Battle, [ Role.Configuration ], self.group_name)
            outline.append_attribute(self.group_name, Dataset.Ranking, [ Role.Configuration ], self.group_name)
        for parameter in self.parameters:
            parameter.outline_simulation(self, simulation, outline)

    def start_simulation(self, simulation):
        """
        Start a simulation
        """
        for parameter in self.parameters:
            parameter.start_simulation(self, simulation)

    def get_group_components(self, member):
        if not self.group_name:
            return []
        simulation = member.simulation
        components = [ c for c in simulation.components if c.group_name == self.group_name ]
        return components

    def get_active_name(self, member):
        """
        Get the name of the group component that is active
        """
        if self.group_name is None:
            # If the component isn't grouped then its the active one!
            return self.name
        active_name = getattr(member.configuration, self.group_name)
        return active_name

    def is_active(self, member):
        """
        Is this component active for the selected member?
        """
        if self.group_name is None:
            # Components that aren't grouped are always active
            return True
        active = self.get_active_name(member) == self.name
        return active

    def start_group(self, member):
        """
        Perform member startup for a component group
        """
        if hasattr(member.configuration, self.group_name):
            raise RuntimeError("Group is already started")

        components = self.get_group_components(member)
        random_state = member.simulation.random_state
        component_index = random_state.randint(0, len(components))
        value = components[component_index].name
        setattr(member.configuration, self.group_name, value)

    def start_member(self, member):
        """
        Start a member
        """
        if not self.group_name is None and not hasattr(member.configuration, self.group_name):
            self.start_group(member)

        if self.is_active(member) and self.parameters:
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
        setattr(member.configuration, self.group_name, prior_group)

    def copy_member(self, member, prior):
        """
        Start a new member by copying an existing member
        """
        if not self.group_name is None:
            self.copy_group(member, prior)
        if self.is_active(member) and self.parameters:
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.copy_member(self, member, prior)

    def mutate_group(self, member):
        configuration = member.configuration
        components = self.get_group_components(member)
        if len(components) < 2:
            return False

        random_state = member.simulation.random_state
        prior_value = getattr(member.configuration, self.group_name)
        attempts = 0
        max_attempts = 50
        mutated = False
        while not mutated:
            choice_index = random_state.randint(0, len(components))
            value = components[choice_index].name
            if value != prior_value:
                mutated = True
            else:
                # We expect things to mutate quickly
                # But make sure we don't get stuck in an infinite loop
                attempts += 1
                if attempts > max_attempts:
                    raise RuntimeError("Attempt to mutate parameter failed")
        
        if hasattr(configuration, prior_value):
            delattr(configuration, prior_value)
        setattr(configuration, self.group_name, value)
        component = [c for c in components if c.name == value][0]
        component.start_member(member)
        return True

    def mutate_member(self, member):
        """
        Mutate a member
        """
        if not self.is_active(member):
            return False

        random_state = member.simulation.random_state
        parameters = self.parameters

        group_name = self.group_name
        n_group = 1 if group_name  else 0
        group_index = 0 if group_name else None
        n_parameters = len(parameters)
        if not n_parameters and not n_group:
            return False

        parameter_indexes = random_state.choice(n_group + n_parameters, size=n_group + n_parameters, replace=False)
        for parameter_index in parameter_indexes:
            if parameter_index == group_index:
                mutated = self.mutate_group(member)
            else:
                parameter = parameters[parameter_index - n_group]
                mutated = parameter.mutate_member(self, member)
            if mutated:
                return True
        return False

    def crossover_member(self, member, parent0, parent1):
        random_state = member.simulation.random_state

        # If we are in group mode and this is the first group
        # pick one of the parents to base my group on and copy it
        if self.group_name and not hasattr(member.configuration, self.group_name):
            parent0_group = self.get_active_name(parent0)
            parent1_group = self.get_active_name(parent1)
            parent_index = random_state.randint(0,2)
            active_name = parent0_group if parent_index == 0 else parent1_group
            setattr(member.configuration, self.group_name, active_name)
        else:
            active_name = self.get_active_name(member)

        if self.parameters and self.group_name and active_name == self.name:
            # We are crossing over the selected component in group mode
            setattr(member.configuration, self.name, SimpleNamespace())
            parent0_group = self.get_active_name(parent0)
            parent1_group = self.get_active_name(parent1)
            if parent0_group == parent1_group:
                # Parents have the same component
                # Do a parameter wise copy
                for parameter in self.parameters:
                    parameter.crossover_member(self, member, parent0, parent1)
            else:
                # Parents don't match
                # Do a copy of the selected parent
                parent = parent0 if parent0_group == active_name else parent1
                for parameter in self.parameters:
                    parameter.copy_member(self, member, parent)
        elif self.parameters and not self.group_name:
            setattr(member.configuration, self.name, SimpleNamespace())
            for parameter in self.parameters:
                parameter.crossover_member(self, member, parent0, parent1)

    def prepare_member(self, member):
        """
        Perform member preparation
        """
        pass

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        pass

    def contest_members(self, member1, member2, outcome):
        """
        Run a contest between two members to determine who is better
        """
        pass

    def stress_members(self, member1, member2, outcome):
        """
        Determine the fate of the members
        """
        pass

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """
        pass

    def rank_members(self, simulation, ranking):
        """
        Rank members in order of importance.
        Only mature, attractive, rated members get a ranking
        """
        pass

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        if not self.is_active(member):
            return None
        if not self.group_name is None:
            setattr(record, self.group_name, self.get_active_name(member))
        for parameter in self.parameters:
            parameter.record_member(self, member, record)

    def record_ranking(self, member, record):
        """
        Record the state of a member
        """
        if not self.is_active(member):
            return None
        if self.group_name:
            setattr(record, self.group_name, self.get_active_name(member))
        for parameter in self.parameters:
            parameter.record_ranking(self, member, record)

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        pass

