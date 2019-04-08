from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

import time
import warnings

class VotingContest(Evaluater):
    """
    Determines fitness by comparing which members increase the score
    of a voting classifier
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def get_score_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "score_evaluation"):
            evaluation.score_evaluation = ScoreEvaluation()
        return evaluation.score_evaluation

    def calculate_voting_predictions(self, members, league):
        """
        Calculate the voting predictions for a list of members
        """
        votes = np.array([ self.get_score_evaluation(m).league_predictions[league].astype(int) for m in members ])
        predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=votes)
        return predictions

    def calculate_score_boost(self, member, base_members, league):
        """
        Calculate the boost that a member gives to the hard voting prediction of a set of stacked members
        """
        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        base_predictions = self.calculate_voting_predictions(base_members, league)
        base_score = scorer.score(y, base_predictions)

        combined_members = base_members + [ member ]
        combined_predictions = self.calculate_voting_predictions(combined_members, league)
        combined_score = scorer.score(y, combined_predictions)

        score_boost = combined_score - base_score
        return score_boost

    def contest_members(self, contestant1, contestant2, outcome):

        contestant1.evaluation.voting_boost = None
        contestant1.evaluation.voting_contest = None
        contestant2.evaluation.voting_boost = None
        contestant2.evaluation.voting_contest = None

        simulation = contestant1.simulation

        top_league = simulation.top_league
        if not top_league in self.get_score_evaluation(contestant1).league_predictions or not top_league in self.get_score_evaluation(contestant2).league_predictions:
            return None

        base_members = [ m for m in simulation.members if m.league == top_league and m.id != contestant1.id and m.id != contestant2.id and top_league in self.get_score_evaluation(m).league_predictions]
        if not base_members:
            return None

        contestant1_boost = self.calculate_score_boost(contestant1, base_members, top_league)
        contestant1.evaluation.voting_boost = contestant1_boost
        contestant2_boost = self.calculate_score_boost(contestant2, base_members, top_league)
        contestant2.evaluation.voting_boost = contestant2_boost

        if contestant1_boost > contestant2_boost:
            contestant1.evaluation.voting_contest = "Win"
            contestant2.evaluation.voting_contest = "Lose"
            contestant1.victory()
            contestant2.defeat()

        if contestant1_boost < contestant2_boost:
            contestant1.evaluation.voting_contest = "Lose"
            contestant2.evaluation.voting_contest = "Win"
            contestant1.defeat()            
            contestant2.victory()

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "voting_boost"):
            record.voting_boost = evaluation.voting_boost
            record.voting_contest = evaluation.voting_contest
        else:
            record.voting_boost = None
            record.voting_contest = None
