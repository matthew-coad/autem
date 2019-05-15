from ..member_manager import MemberManager
from .decision_grid_state import DecisionGridState
from .tune_settings import TuneSettings

class GridSpotcheck(MemberManager):
    """
    Spotchecker that introduces decision in an orderly grid.

    This spotcheck is used when evaluating components.
    """

    def configure_member(self, member):
        """
        Configure new members by setting them to outstanding decisions
        """

        spotchecking = TuneSettings(member).get_spotchecking()
        if spotchecking is not None and not spotchecking:
            return (None, None)

        settings = SimulationSettings(member)
        specie = member.get_specie()
        outstanding_decisions = DecisionGridState.get(specie).list_outstanding_decisions()
        if not outstanding_decisions:
            return (None, None)

        decision = outstanding_decisions[0]
        member.set_decision(decision)
        DecisionGridState.get(specie).introduce_decision(decision)
           
        specialized, reason = member.specialize()
        return (specialized, reason)
