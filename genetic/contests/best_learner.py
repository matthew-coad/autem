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

    def contest_members(self, contestant1, contestant2, outcome):

        if outcome.is_conclusive():
            return None

        required_p_value = self.p_value

        member1_scores = np.array(contestant1.accuracies)
        member2_scores = np.array(contestant2.accuracies)

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

        t_statistic = test_result[0] # positive if 1 > 2
        maturity = test_result[1]
        mature = 1 if maturity <= required_p_value else 0

        contestant1.maturing(maturity, mature)
        contestant2.maturing(maturity, mature)

        # Need at least the required p-value to have an outcome
        if maturity > required_p_value:
            outcome.inconclusive()
            return None

        # TODO Differentiate between decisive and indecisive
        if t_statistic > 0:
            outcome.decisive(1)
        else:
            outcome.decisive(2)

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """

        if not member.rating is None:
            # Don't rerate! It's expensive
            return None
        simulation = member.simulation
        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_divided()
        pipeline = member.evaluation.pipeline
        scores = cross_val_score(pipeline, x, y, scoring=scorer.scoring, cv=10)

        rating = scores.mean()
        rating_sd = scores.std()
        member.rate(rating, rating_sd)

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

    