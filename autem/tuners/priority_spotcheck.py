from ..member_manager import MemberManager
from .decision_grid_state import DecisionGridState
from ..simulation_settings import SimulationSettings

class PrioritySpotcheck(MemberManager):
    """
    Spot checker that introduces members based on the decision priority.
    """

    def configure_random_member(self, member):
        """
        Configure new members by setting them to outstanding decisions
        """

        settings = SimulationSettings(member)
        specie = member.get_specie()
        outstanding_decisions = DecisionGridState.get(specie).list_outstanding_decisions()
        if not outstanding_decisions:
            return (None, None)
            
        decision_index = settings.get_random_state().randint(0, len(outstanding_decisions))
        decision = outstanding_decisions[decision_index]
        member.set_decision(decision)
        DecisionGridState.get(specie).introduce_decision(decision)
           
        specialized, reason = member.specialize()
        return (specialized, reason)

    def configure_member(self, member):
        specie = member.get_specie()
        decision_grid_state = DecisionGridState.get(specie)
        if not decision_grid_state.get_prioritised():
            return self.configure_random_member(member)

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
