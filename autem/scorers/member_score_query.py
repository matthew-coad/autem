from ..member import Member
from .member_score_state import MemberScoreState
from ..simulation_settings import SimulationSettings
from .score_query import ScoreQuery

class MemberScoreQuery(ScoreQuery):

    def __init__(self, member):
        assert isinstance(member, Member)
        ScoreQuery.__init__(self, member)

    def _get_score_state(self):
        return MemberScoreState.get(self.get_container())

    def get_score(self):
        """
        Get the best available score for the member
        """
        return self._get_score_state().score

    def get_score_std(self):
        """
        Get the best available score std for the member
        """
        return self._get_score_state().score_std

    def get_duration(self):
        """
        Get how it long it took to evaluate each fit
        """
        return self._get_score_state().score_duration

    def get_duration_std(self):
        """
        Get the standard deviation of how long it took to evaluate each fit
        """
        return self._get_score_state().score_duration_std        

    def get_score_std(self):
        """
        Get the best available score std for the member
        """
        return self._get_score_state().score_std

    def get_high_score(self):
        """
        Get the upper score of the 60% confidence interval
        """
        score_std = self.get_score_std()
        if score_std is None:
            return None
        return self.get_score() + score_std

    def get_upper_score(self):
        """
        Get the upper score of the 95% confidence interval
        """
        score_std = self.get_score_std()
        if score_std is None:
            return None
        return self.get_score() + 2 * score_std

    def get_low_score(self):
        """
        Get the lower score of the 60% confidence interval
        """
        score_std = self.get_score_std()
        if score_std is None:
            return None
        return self.get_score() - score_std

    def get_lower_score(self):
        """
        Get the lower score of the 95% confidence interval
        """
        score_std = self.get_score_std()
        if score_std is None:
            return None
        return self.get_score() - 2 * score_std

    def get_league(self):
        """
        Get the members league level
        """
        return self.get_container().league

    def get_max_league(self):
        """
        Get the maximum permitted league level
        """
        return SimulationSettings(self.get_container()).get_max_league()

    def is_rookie(self):
        """
        Is the member a rookie?

        Rookies have a league level of 0. Rookies have inaccurate scores and are unlikely
        to be a contender
        """
        return self.get_league() == 0

    def is_veteran(self):
        """
        Is the member a veteran?

        Veterans have the maximum league level. Have the most accurates scores and
        are likely to be a possible solution
        """
        return self.get_league() == self.get_max_league()

    def is_pro(self):
        """
        Is the member a pro?

        Pros are in the upper levels. Have reasonably accurate scores.
        """
        return self.get_league() >= 2

    # League level queries

    def has_league_predictions(self, league):
        return league in self._get_score_state().league_predictions

    def get_league_predictions(self, league):
        return self._get_score_state().league_predictions[league]
