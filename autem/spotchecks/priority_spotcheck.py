from ..member_manager import MemberManager
from .decision_grid_state import DecisionGridState

class PrioritySpotcheck(MemberManager):
    """
    Spot checker that introduces members based on the decision priority.
    """

    def configure_member(self, member):
        specie = member.get_specie()
        decision_grid_state = DecisionGridState.get(specie)
        if not decision_grid_state.get_prioritised():
            return (None, None)

        outstanding_decisions = decision_grid_state.list_outstanding_decisions()
        if not outstanding_decisions:
            return (None, None)

        priorities = [ decision_grid_state.get_decision_priority(d) for d in outstanding_decisions ]
        decision_index = priorities.index(max(priorities))
        decision = outstanding_decisions[decision_index]
        member.set_decision(decision)
        decision_grid_state.introduce_decision(decision)
        specialized, reason = member.specialize()
        return (specialized, reason)
