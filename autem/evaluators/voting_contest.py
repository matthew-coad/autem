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

    def evaluate_member(self, member):
        """
        Evaluate the cross validated predictions for the given member
        provided it is at the maximum league level
        """
        simulation = member.simulation
        resources = member.resources
        evaluation = member.evaluation
        loader = simulation.resources.loader
        estimator = resources.pipeline

        top_league = simulation.top_league
        if member.league < top_league:
            return None

        if hasattr(evaluation, "predictions"):
            return None

        x,y = loader.load_training_data(simulation)

        start = time.time()

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                predictions = cross_val_predict(estimator, x, y, cv=5)
            except Exception as ex:
                member.fail(ex, "evaluate_predictions", "DiversityContest")
                return None

        end = time.time()
        duration = end - start

        evaluation.predictions = predictions
        evaluation.prediction_duration = duration

    def calculate_voting_predictions(self, members):
        """
        Calculate the voting predictions for a list of members
        """
        votes = np.array([ m.evaluation.predictions for m in members ])
        predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=votes)
        return predictions

    def calculate_score_boost(self, member, base_members):
        """
        Calculate the boost that a member gives to the hard voting prediction of a set of stacked members
        """
        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        base_predictions = self.calculate_voting_predictions(base_members)
        base_score = scorer.score(y, base_predictions)

        combined_members = base_members + [ member ]
        combined_predictions = self.calculate_voting_predictions(combined_members)
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
        if contestant1.league < top_league or contestant2.league < top_league:
            return None

        if not hasattr(contestant1.evaluation, "predictions") or not hasattr(contestant2.evaluation, "predictions"):
            return None

        base_members = [ m for m in simulation.members if m.league == top_league and m.id != contestant1.id and m.id != contestant2.id and hasattr(m.evaluation, "predictions")]
        if not base_members:
            return None

        contestant1_boost = self.calculate_score_boost(contestant1, base_members)
        contestant1.evaluation.voting_boost = contestant1_boost
        contestant2_boost = self.calculate_score_boost(contestant2, base_members)
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
