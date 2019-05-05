from .hyper_parameter import HyperParameter
from .reporters import DataType, Role, Reporter
from .simulation_settings import SimulationSettings

class Parameter(HyperParameter, Reporter):

    def __init__(self, name, label, type, shared = False):
        HyperParameter.__init__(self, name)
        self.label = label
        self.type = type
        self.shared = shared

        if not type in ["nominal", "numeric"]:
            raise RuntimeError("Type is not valid")

    def get_initial_value(self, member):
        raise NotImplementedError()

    def get_mutated_value(self, member):
        raise NotImplementedError()

    def get_configuration(self, member):
        if not self.get_group_name():
            raise RuntimeError("Group not selected")
        return getattr(member.configuration, self.get_group_name())

    def has_configuration(self, member):
        if not self.get_group_name():
            raise RuntimeError("Group not selected")
        return hasattr(member.configuration, self.get_group_name())

    def get_value(self, member):
        return getattr(self.get_configuration(member), self.get_name())

    def set_value(self, member, value):
        return setattr(self.get_configuration(member), self.get_name(), value)

    def get_record_name(self):
        if not self.shared:
            if not self.get_group_name():
                raise RuntimeError("Group not selected")
            record_name = "%s_%s" % (self.get_group_name(), self.get_name())
        else:
            if not self.get_choice_name():
                raise RuntimeError("Choice not selected")
            record_name = "%s_%s" % (self.get_choice_name(), self.get_name())
        return record_name

    def outline_simulation(self, simulation, outline):
        record_name = self.get_record_name()
        if not outline.has_attribute(record_name, DataType.Battle):
            outline.append_attribute(self.get_record_name(), DataType.Battle, [ Role.Parameter ], self.label)

    def record_member(self, member, record):
        if self.has_configuration(member):
            setattr(record, self.get_record_name(), self.get_value(member))
        else:
            setattr(record, self.get_record_name(), None)

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
        random_state = SimulationSettings(member).get_random_state()
        parent_index = random_state.randint(0, 2)
        parent = parent0 if parent_index == 0 else parent1
        value = self.get_value(parent)
        self.set_value(member, value)

