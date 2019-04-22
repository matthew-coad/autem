from .maker import Maker
from ..choice import Choice

class CrossoverMaker(Maker):
    """
    Makes new members by a cross over operation
    """

    def configure_member(self, member):
        specie = member.get_specie()
        candidates = specie.list_members(alive = True, top = True)
        if len(candidates) < 2:
            candidates = specie.list_members(alive = True)
        if len(candidates) < 2:
            return False
        parent_indexes = specie.get_random_state().choice(len(candidates), 2, replace = False)
        parent1 = candidates[parent_indexes[0]]
        parent2 = candidates[parent_indexes[1]]
        for component in specie.list_hyper_parameters():
            component.crossover_member(member, parent1, parent2)
        return True
