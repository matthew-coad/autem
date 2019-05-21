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

    def _get_league_score_state(self):
        """
        Get the current league score state
        """
        score_state = self._get_score_state()
        if score_state.current_league is None:
            return None
        return score_state.leagues[score_state.current_league]

    def get_score(self):
        """
        Get the best available score for the member
        """
        if self.get_current_league() is None:
            return None
        return self._get_league_score_state().score

    def get_score_std(self):
        """
        Get the best available score std for the member
        """
        if self.get_current_league() is None:
            return None
        return self._get_league_score_state().score_std

    def get_duration(self):
        """
        Get how it long it took to evaluate each fit
        """
        if self.get_current_league() is None:
            return None
        return self._get_league_score_state().duration

    def get_duration_std(self):
        """
        Get the standard deviation of how long it took to evaluate each fit
        """
        if self.get_current_league() is None:
            return None
        return self._get_league_score_state().duration_std

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

    def get_current_league(self):
        """
        Get the currently active, evaluated league level
        """
        score_state = self._get_score_state()
        return score_state.current_league

    def is_rookie(self):
        """
        Is the member a rookie?

        Rookies have a league level of 0. Rookies have inaccurate scores and are unlikely
        to be a contender
        """
        current_league = self.get_current_league()
        return current_league is None or current_league == 0

    def is_veteran(self):
        """
        Is the member a veteran?

        Veterans have the maximum league level. Have the most accurates scores and
        are likely to be a possible solution
        """
        if self.get_current_league() is None:
            return False
        return self.get_current_league() == self.get_n_leagues() - 1

    def is_pro(self):
        """
        Does this league have
        """
        # Its a pro if the number of scores 
        if self.get_current_league() is None:
            return False
        return len(self._get_league_score_state().scores) >= self.get_n_folds()

    # League level queries

    def has_league_scores(self, league):
        """
        Do we have scores a given league level?
        """
        return league in self._get_score_state().leagues

    def get_league_score(self, league):
        return self._get_score_state().leagues[league].score

    def get_league_duration(self, league):
        return self._get_score_state().leagues[league].duration

    def get_league_predictions(self, league):
        return self._get_score_state().leagues[league].predictions

