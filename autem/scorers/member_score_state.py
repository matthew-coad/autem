from ..member import Member

class MemberScoreState:

    def __init__(self):
        self.leagues = {} # Scoring state for each league
        self.current_league = None # Current scoring league

    def get(member):
        assert isinstance(member, Member)
        return member.get_state("member_score", lambda: MemberScoreState())
