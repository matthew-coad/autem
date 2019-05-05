from ..member_manager import MemberManager
from ..choice import Choice
from ..scorers import MemberLeagueState
from .decision_grid_state import DecisionGridState
from ..simulation_settings import SimulationSettings

from .tune_settings import TuneSettings

class CrossoverSpotcheck(MemberManager):
    """
    Introduces new members by crossing over existing members
    """

    def configure_member(self, member):

        tuning = TuneSettings(member).get_tuning()
        if tuning is not None and tuning:
            return (None, None)

        settings = SimulationSettings(member)
        specie = member.get_specie()
        members = specie.list_members(alive = True)
        candidates = [ m for m in members if MemberLeagueState.get(m).is_pro() ]
        if len(candidates) < 2:
            return (None, None)
        parent_indexes = settings.get_random_state().choice(len(candidates), 2, replace = False)
        parent1 = candidates[parent_indexes[0]]
        parent1_decision = parent1.get_decision()
        parent2 = candidates[parent_indexes[1]]
        parent2_decision = parent2.get_decision()
        parent_decisions = list(zip(parent1.get_decision(), parent2.get_decision()))
        indices = settings.get_random_state().choice(2, len(parent_decisions), replace = True)
        decision = tuple(parent_decisions[i][indices[i]] for i in range(len(parent_decisions)))
        introductions = DecisionGridState.get(specie).get_decision_introductions(decision)

        if introductions > 0:
            return (None, None)

        member.set_decision(decision)
        DecisionGridState.get(specie).introduce_decision(decision)
        specialized, reason = member.specialize()
        return (specialized, reason)
