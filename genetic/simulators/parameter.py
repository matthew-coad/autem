from .dataset import Dataset

class Parameter:

    def __init__(self, name, role, label):
        self.name = name
        self.role = Role
        self.label = label

    def get_start_value(self, component, member):
        raise NotImplementedError()

    def get_mutated_value(self, component, member):
        raise NotImplementedError()

    def get_configuration(self, component, member):
        return getattr(member.configuration, component.name)

    def get_value(self, component, member):
        return getattr(self.get_configuration(component, member), self.name)

    def set_value(self, component, member, value):
        return setattr(self.get_configuration(component, member), self.name, value)

    def get_record_name(self, component):
        return "%s_%s" % (component.name, self.name)

    def outline_simulation(self, component, simulation, outline):
        outline.append_attribute(self.get_record_name(component), Dataset.Battle, self.role , self.label)
        outline.append_attribute(self.get_record_name(component), Dataset.Ranking, self.role , self.label)

    def start_simulation(self, component, simulation):
        pass

    def start_member(self, component, member):
        self.set_value(component, member, self.get_start_value(component, member))

    def start_member(self, component, member):
        self.set_value(component, member, self.get_start_value(component, member))

    def copy_member(self, component, member, prior):
        self.set_value(component, member, self.get_value(component, prior))

    def mutate_member(self, component, member):
        prior_value = self.get_value(component, member)
        attempts = 0
        max_attempts = 50
        mutated = False
        while True:
            value = self.get_mutated_value(component, member)
            if value != prior_value:
                self.set_value(component, member, value)
                return True

            # We expect things to mutate quickly
            # But make sure we don't get stuck in an infinite loop
            attempts += 1
            if attempts > max_attempts:
                raise RuntimeError("Attempt to mutate parameter failed")
        return False

    def crossover_member(self, component, member, parent0, parent1):
        random_state = member.simulation.random_state
        parent_index = random_state.randint(0, 2)
        parent = parent0 if parent_index == 0 else parent1
        value = self.get_value(component, parent)
        self.set_value(component, member, value)

    def record_member(self, component, member, record):
        setattr(record, self.get_record_name(component), self.get_value(component, member))

