from ..simulators import Dataset, Role
from .contester import Contester

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class BestLearner(Contester):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        Contester.__init__(self, "BestLearner")
        self.p_value = p_value

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        outline.append_attribute("contest_p", Dataset.Battle, [Role.Measure], "contest p value")

    def evaluate_member(self, member, evaluation):
        super().evaluate_member(member, evaluation)
        if not self.is_active(member):
            return None

        prior_evaluation = member.evaluation
        if hasattr(prior_evaluation, "cross_val_scores"):
            member.evaluation.cross_val_scores = prior_evaluation.cross_val_scores
            member.evaluation.cross_val_mean = prior_evaluation.cross_val_mean
            member.evaluation.cross_val_sd = prior_evaluation.cross_val_sd

    def contest_members(self, contestant1, contestant2, outcome):

        # Make sure we define these extension values
        outcome.t_statistic = None
        outcome.p_value = None

        if outcome.is_conclusive():
            return None

        if not contestant1.evaluation is None:
            member1_scores = np.array(contestant1.evaluation.test_scores)
        else:
            member1_scores = np.array([])
        if not contestant2.evaluation is None:
            member2_scores = np.array(contestant2.evaluation.test_scores)
        else:
            member2_scores = np.array([])
        required_p_value = self.p_value

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            outcome.inconclusive()
            return None

        # Run the t-test
        try:
            test_result = stats.ttest_ind(member1_scores, member2_scores)
        except:
            outcome.inconclusive()
            return None

        outcome.t_statistic = test_result[0] # positive if 1 > 2
        outcome.p_value = test_result[1]

        # Need at least the required p-value to have an outcome
        if outcome.p_value > required_p_value:
            outcome.inconclusive()
            return None

        # TODO Differentiate between decisive and indecisive
        if outcome.t_statistic > 0:
            outcome.decisive(1)
        else:
            outcome.decisive(2)

    def evaluate_cross_val_score(self, simulation, member):

        if hasattr(member.evaluation, "cross_val_scores"):
            return None

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_divided()
        pipeline = member.evaluation.pipeline
        scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=10)
        member.evaluation.cross_val_scores = scores
        member.evaluation.cross_val_mean = scores.mean()
        member.evaluation.cross_val_sd = scores.std()

    def rank_members(self, simulation, ranking):

        super().record_ranking(simulation, ranking)

        # To qualify for ranking a member must be
        # Be alive and attractive 

        candidates = [m for m in simulation.members if m.alive == 1 and m.attractive == 1]
        if not candidates:
            ranking.inconclusive()
            return None

        for candidate in candidates:
            self.evaluate_cross_val_score(simulation, candidate)

        candidates = sorted(candidates, key=lambda member: member.evaluation.cross_val_mean, reverse=True)
        ranking.conclusive(candidates)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        super().record_member(member, record)
        if not self.is_active(member):
            return None

        contest = member.contest
        record.contest_p = contest.p_value if contest else None

    def record_ranking(self, member, record):
        """
        Record information for the ranking
        """
        super().record_ranking(member, record)
        if not self.is_active(member):
            return None

        record.score = member.evaluation.cross_val_mean
        record.score_sd = member.evaluation.cross_val_sd


