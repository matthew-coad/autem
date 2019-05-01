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

    def get_score(self):
        """
        Get the best available score for the member
        """
        return self.score

    def get_high_score(self):
        """
        Get the upper score of the 60% confidence interval
        """
        if self.score_std is None:
            return None
        return self.score + self.score_std

    def get_upper_score(self):
        """
        Get the upper score of the 95% confidence interval
        """
        if self.score_std is None:
            return None
        return self.score + 2 * self.score_std

    def get_low_score(self):
        """
        Get the lower score of the 60% confidence interval
        """
        if self.score_std is None:
            return None
        return self.score - self.score_std

    def get_lower_score(self):
        """
        Get the lower score of the 95% confidence interval
        """
        if self.score_std is None:
            return None
        return self.score - 2 * self.score_std

    def get(container):
        return container.get_state("member_score", lambda: MemberScoreState())

