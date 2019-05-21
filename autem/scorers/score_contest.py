from ..member_manager import MemberManager

from .score_query import ScoreQuery
from .member_score_query import MemberScoreQuery
from .metrics import accuracy_score

class ScoreContest(MemberManager):

    def __init__(self, verify_accuracy = 1.0):
        MemberManager.__init__(self)
        self.verify_accuracy = verify_accuracy

    # Contests

    def contest_veterans(self, contestant1, contestant2):
        """
        Evaluate a contest between two veterans
        """

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

        # If scores are equal there is no outcome
        if contestant1_scores.get_score() == contestant2_scores.get_score():
            return
        winner = contestant1 if contestant1_scores.get_score() > contestant2_scores.get_score() else contestant2
        loser = contestant1 if contestant1_scores.get_score() < contestant2_scores.get_score() else contestant2
        winner.victory()
        loser.defeat()

    def contest_peers(self, contestant1, contestant2):
        """
        Evaluate a contest between peers, IE are at the same league but not veterans or rookies
        """

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

        # If scores are equal there is no outcome
        if contestant1_scores.get_score() == contestant2_scores.get_score():
            return

        pros = contestant1_scores.is_pro()
        # If the score of one contestant is inside the 60% confidence interval of the other then their is no outcome
        if pros and contestant1_scores.get_low_score() <= contestant2_scores.get_score() <= contestant1_scores.get_high_score():
            return

        # If the score of one contestant is inside the 95% confidence interval of the other then their is no outcome
        if not pros and contestant1_scores.get_lower_score() <= contestant2_scores.get_score() <= contestant1_scores.get_upper_score():
            return

        # Their is clear seperation so we can determine an outcome
        winner = contestant1 if contestant1_scores.get_score() > contestant2_scores.get_score() else contestant2
        loser = contestant1 if contestant1_scores.get_score() < contestant2_scores.get_score() else contestant2
        winner.victory()
        loser.defeat()

    def contest_mismatch(self, contestant1, contestant2):
        """
        Evaluate a mismatch, where the contestants are at different league levels
        """
        contestant1_leagues = MemberScoreQuery(contestant1)
        contestant2_leagues = MemberScoreQuery(contestant2)

        # Determine who is the senior and who is the junior
        senior = contestant1 if contestant1_leagues.get_current_league() > contestant2_leagues.get_current_league() else contestant2
        junior = contestant1 if contestant1_leagues.get_current_league() < contestant2_leagues.get_current_league() else contestant2
        pros = MemberScoreQuery(junior).is_pro()

        # If scores are equal there is no outcome
        senior_scores = MemberScoreQuery(senior)
        junior_scores = MemberScoreQuery(junior)

        # If they are pros and the score of the junior is inside the 60% confidence interval of the senior then their is no outcome
        if pros and senior_scores.get_low_score() <= junior_scores.get_score() <= senior_scores.get_high_score():
            return

        # If they are not both pros and the score of the junior is inside the 95% confidence interval of the senior then their is no outcome
        if not pros and senior_scores.get_lower_score() <= junior_scores.get_score() <= senior_scores.get_upper_score():
            return

        # Their is clear seperation so we can determine an outcome
        winner = senior if senior_scores.get_score() > junior_scores.get_score() else junior
        loser = senior if senior_scores.get_score() < junior_scores.get_score() else junior
        winner.victory()
        loser.defeat()

    def verify_unique(self, contestant1, contestant2):

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

        if not contestant1_scores.is_pro() or not contestant2_scores.is_pro():
            return True

        league = min(contestant1_scores.get_current_league(), contestant2_scores.get_current_league())

        contestant1_predictions = contestant1_scores.get_league_predictions(league)
        contestant2_predictions = contestant2_scores.get_league_predictions(league)
        inter_score = accuracy_score(contestant1_predictions, contestant2_predictions)
        if inter_score < self.verify_accuracy:
            return True

        # The contestants make nearly identical predictions
        # kill one
        if contestant1.league < contestant2.league:
            contestant1.kill("Senior Identical")
        elif contestant1.league > contestant2.league:
            contestant2.kill("Senior Identical")
        elif contestant1.id < contestant2.id:
            contestant2.kill("Earlier Identical")
        elif contestant1.id > contestant2.id:
            contestant1.kill("Earlier Identical")
        else:
            raise RuntimeError("Unexpected condition")
        return False

    def contest_members(self, contestant1, contestant2):

        verified = self.verify_unique(contestant1, contestant2)
        if not verified:
            return 

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

        # If both members are rookies then the scores are too inaccurate to make a judgement
        if contestant1_scores.is_rookie() and contestant2_scores.is_rookie():
            return

        # If both members are veterans then we can use the veteran test
        if contestant1_scores.is_veteran() and contestant2_scores.is_veteran():
            self.contest_veterans(contestant1, contestant2)
            return

        # If both members are on the same league then we can use the peers test
        if contestant1_scores.get_current_league() == contestant2_scores.get_current_league():
            self.contest_peers(contestant1, contestant2)
            return

        # Otherwise make the mismatch test
        self.contest_mismatch(contestant1, contestant2)
