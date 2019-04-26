from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

import time
import warnings

class VotingEvaluation:

    def __init__(self):
        self.base_score = None
        self.combined_score = None
        self.score_boost = None
        self.evaluated = False
        self.victories = 0

def get_voting_evaluation(member):
    """
     Get voting evaluation for a member
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "voting_evaluation"):
        evaluation.voting_evaluation = VotingEvaluation()
    return evaluation.voting_evaluation


class VotingContest(Evaluater):
    """
    Determines fitness by comparing which members increase the score
    of a voting classifier
    """

    def calculate_voting_predictions(self, members, league):
        """
        Calculate the voting predictions for a list of members
        """
        votes = np.array([ get_score_resources(m).league_predictions[league].astype(int) for m in members ])
        predictions = np.apply_along_axis(lambda x: np.argmax(np.bincount(x)), axis=0, arr=votes)
        return predictions

    def calculate_voting_evaluation(self, member, base_members, league):
        """
        Calculate the boost that a member gives to the hard voting prediction of a set of stacked members
        """
        scorer = member.get_simulation().get_scorer()

        data = member.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        base_predictions = self.calculate_voting_predictions(base_members, league)
        base_score = scorer.score(y, base_predictions)

        combined_members = [ member ] + base_members
        combined_predictions = self.calculate_voting_predictions(combined_members, league)
        combined_score = scorer.score(y, combined_predictions)

        score_boost = combined_score - base_score

        voting_evaluation = VotingEvaluation()
        voting_evaluation.base_score = base_score
        voting_evaluation.combined_score = combined_score
        voting_evaluation.score_boost = score_boost
        voting_evaluation.evaluated = True
        return voting_evaluation

    def evaluate_base_members(self, member):
        """
        Voting base members are the top scorers for all of the prior species
        """
        specie = member.get_specie()
        simulation = specie.get_simulation()
        base_members = [ s.get_ranking().get_top_member() for s in simulation.list_species() if s.id != specie.id and s.get_ranking().is_conclusive() ]
        return base_members

    def evaluate_member(self, member):

        voting_evaluation = get_voting_evaluation(member)
        if voting_evaluation.evaluated:
            return None

        if not 1 in get_score_resources(member).league_predictions:
            return None

        base_members = self.evaluate_base_members(member)
        if not base_members:
            voting_evaluation.evaluated = True
            return None

        member.evaluation.voting_evaluation = self.calculate_voting_evaluation(member, base_members, 1)

    def prepare_epoch(self, epoch):
        for member in epoch.list_members(alive = True):
            votes = get_voting_evaluation(member)
            votes.victories = 0

    def contest_members(self, contestant1, contestant2):

        specie = contestant1.get_specie()
        epoch = specie.get_current_epoch()

        contestant1_votes = get_voting_evaluation(contestant1)
        contestant2_votes = get_voting_evaluation(contestant2)

        if contestant1_votes.score_boost is None or contestant2_votes.score_boost is None:
            return None

        if contestant1_votes.score_boost == contestant2_votes.score_boost:
            return None

        if contestant1_votes.score_boost > contestant2_votes.score_boost:
            contestant1.victory()
            contestant1_votes.victories += 1
            contestant2.defeat()
        else:
            contestant1.defeat()
            contestant2.defeat()
            contestant2_votes.victories += 1

    def record_member(self, member, record):
        super().record_member(member, record)

        voting_evaluation = get_voting_evaluation(member)
        record.VC_boost = voting_evaluation.score_boost
        record.VC_victories = voting_evaluation.victories
