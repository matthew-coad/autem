from . import components

from types import SimpleNamespace

class Member:
    """
    Member of a population
    """
    def __init__(self, population, parent0 = None, parent1 = None): 
        self.id = population.simulation.generate_id()
        self.simulation = population.simulation
        self.population = population
        self.history = SimpleNamespace()
        self.configuration = SimpleNamespace()
        self.evaluation = SimpleNamespace()

        if not parent0 is None and not parent1 is None:
            self.parent0id = parent0.id
            self.parent1id = parent1.id
            for component in self.simulation.components:
                component.crossoverMember(self, parent0, parent1)
        elif not parent0 is None:
            self.parent0id = parent0.id
            self.parent1id = 0
            for component in self.simulation.components:
                component.copyMember(self, parent0)
        else:
            self.parent0id = 0
            self.parent1id = 0
            for component in self.simulation.components:
                component.initializeMember(self)

    def mutate(self):
        random_state = self.simulation.random_state
        components = self.simulation.components
        n_components = len(components)

        # Randomly select components to attempt to mutate
        component_indexes = random_state.choice(n_components, n_components, replace=False)

        for index in component_indexes:
            component = components[index]
            mutated = component.mutateMember(self)
            if mutated:
                break

    def evaluate(self):
        for component in self.simulation.components:
            component.evaluateMember(self)

    def report(self):
        row = SimpleNamespace()
        row.generation_prop = self.population.generation
        row.population_id = self.population.id
        row.member_id = self.id
        row.parent0_id = self.parent0id
        row.parent1_id = self.parent1id
        for component in self.simulation.components:
            component.reportMember(self, row)
        return row
