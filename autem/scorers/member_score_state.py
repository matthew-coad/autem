from ..member import Member

class MemberScoreState:

    def __init__(self):
        self.quick_score = None
        self.quick_duration = None
        self.quick_predictions = None

        self.league_scores = {}
        self.league_durations = {}
        self.league_predictions = {}
        self.league_predictions = {}

        self.scores = []
        self.score = None
        self.score_std = None

        self.score_durations = []
        self.score_duration = None
        self.score_duration_std = None

    def get(member):
        assert isinstance(member, Member)
        return member.get_state("member_score", lambda: MemberScoreState())
