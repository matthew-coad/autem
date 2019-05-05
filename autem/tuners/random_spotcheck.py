from ..member_manager import MemberManager

from .decision_grid_state import DecisionGridState

class RandomSpotcheck(MemberManager):
    """
    Spotchecker that introduces decisions randomly.

    This is used to get an analysis started.
    """

    def configure_member(self, member):
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


