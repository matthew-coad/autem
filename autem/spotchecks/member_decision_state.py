from ..member import Member

class MemberDecisionState:

    """
    State information regarding decision models for a member
    """

    def __init__(self):
        self.reset()

    def get_decision_score(self):
        """
        Get decision score
        """
        return self._decision_score

    def get_evaluated(self):
        return self._evaluated

    def evaluated(self, decision_score):
        """
        Set the state as evaluated
        """
        self._decision_score = decision_score
        self._evaluated = True

    def reset(self):
        """
        Reset the decision state.
        """
        self._evaluated = False
        self._decision_score = None

    def get(member):
        """
        Get decision state for a member
        """
        assert isinstance(member, Member)
        return member.get_state("member_decision", lambda: MemberDecisionState())
