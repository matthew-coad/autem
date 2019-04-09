from .. import Maker, Member, Controller, Choice

class CrossoverMaker(Maker, Controller):
    """
    Makes new members by a cross over operation
    """

    def make_member(self, simulation):
        candidates = simulation.list_members(alive = True)
        if len(candidates) < 2:
            return None
        parent_indexes = simulation.random_state.choice(len(candidates), 2, replace = False)
        parent1 = candidates[parent_indexes[0]]
        parent2 = candidates[parent_indexes[1]]
        member = Member(simulation)
        for component in simulation.hyper_parameters:
            component.crossover_member(member, parent1, parent2)
        specialized = simulation.specialize_member(member)
        if not specialized:
            member = None
        return member
