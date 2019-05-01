from ..member import Member

class MemberLeagueState:

    def __init__(self, league, max_league):
        self._league = league
        self._max_league = max_league

    def get_league(self):
        """
        Get the members league level
        """
        return self._league

    def get_max_league(self):
        """
        Get the maximum permitted league level
        """
        return self._max_league

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

    def get(member):
        assert isinstance(member, Member)
        return MemberLeagueState(member.league, member.get_specie().get_max_league())