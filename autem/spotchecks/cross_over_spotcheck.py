from ..member_manager import MemberManager
from ..choice import Choice
from ..scorers import MemberLeagueState
from .decision_grid_state import DecisionGridState

class CrossoverSpotcheck(MemberManager):
    """
    Introduces new members by crossing over existing members
    """

    def configure_member(self, member):
        specie = member.get_specie()
        members = specie.list_members(alive = True)
        candidates = [ m for m in members if MemberLeagueState.get(m).is_pro() ]
        if len(candidates) < 2:
            return (None, None)
        parent_indexes = specie.get_random_state().choice(len(candidates), 2, replace = False)
        parent1 = candidates[parent_indexes[0]]
        parent2 = candidates[parent_indexes[1]]
        parent_decisions = list(zip(parent1.get_decision(), parent2.get_decision()))
        indices = member.get_random_state().choice(2, len(parent_decisions), replace = True)
        decision = tuple(parent_decisions[i][indices[i]] for i in range(len(parent_decisions)))
        member.set_decision(decision)
        DecisionGridState.get(specie).introduce_decision(decision)
        specialized, reason = member.specialize()
        return (specialized, reason)
