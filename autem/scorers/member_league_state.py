class MemberLeagueState:
    """
    Contains state information for a member relating to a specific league
    """

    def __init__(self, league):
        self.league = league
        self.fits = []
        self.score = None
        self.scores = None
        self.score_std = None
        self.duration = None
        self.durations = None
        self.duration_std = None
        self.predictions = None
