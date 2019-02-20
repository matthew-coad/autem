from .dataset import Dataset
from .role import Role
from .component import Component

class Parameter(Component):

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.group_name = None

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

    def get_initial_value(self, member):
        raise NotImplementedError()

    def get_mutated_value(self, member):
        raise NotImplementedError()

    def get_configuration(self, member):
        if not self.group_name:
            raise RuntimeError("Group not selected")
        return getattr(member.configuration, self.group_name)

    def get_value(self, member):
        return getattr(self.get_configuration(member), self.name)

    def set_value(self, member, value):
        return setattr(self.get_configuration(member), self.name, value)

    def get_record_name(self):
        if not self.group_name:
            raise RuntimeError("Group not selected")
        return "%s_%s" % (self.group_name, self.name)

    def outline_simulation(self, simulation, outline):
        outline.append_attribute(self.get_record_name(), Dataset.Battle, [ Role.Parameter ], self.label)

    def record_member(self, member, record):
        setattr(record, self.get_record_name(), self.get_value(member))

    def initialize_member(self, member):
        value = self.get_initial_value(member)
        self.set_value(member, value)

    def copy_member(self, member, prior):
        self.set_value(member, self.get_value(prior))

    def mutate_member(self, member):
        prior_value = self.get_value(member)
        attempts = 0
        max_attempts = 50
        mutated = False
        while True:
            value = self.get_mutated_value(member)
            if value != prior_value:
                self.set_value(member, value)
                return True

            # We expect things to mutate quickly
            # But make sure we don't get stuck in an infinite loop
            attempts += 1
            if attempts > max_attempts:
                raise RuntimeError("Attempt to mutate parameter failed")
        return False

    def crossover_member(self, member, parent0, parent1):
        random_state = member.simulation.random_state
        parent_index = random_state.randint(0, 2)
        parent = parent0 if parent_index == 0 else parent1
        value = self.get_value(parent)
        self.set_value(member, value)

