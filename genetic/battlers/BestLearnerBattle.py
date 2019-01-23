from .battler import Battler

import numpy as np
from scipy import stats

class BestLearnerBattle(Battler):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def battle_members(self, contestant1, contestant2, result):

        member1_scores = np.array([e.test_score for e in contestant1.evaluations])
        member2_scores = np.array([e.test_score for e in contestant2.evaluations])
        required_p_value = self.p_value

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            result.inconclusive()
            return None

        # Run the t-test
        test_result = stats.ttest_ind(member1_scores, member2_scores)
        t_statistic = test_result[0] # positive if 1 > 2
        p_value = test_result[1]

        # Record the best p-value for each model
        #if member1.evaluation.model_p_value > p_value:
        #    member1.evaluation.model_p_value  = p_value
        #if member2.evaluation.model_p_value > p_value:
        #    member2.evaluation.model_p_value  = p_value

        # Need at least the required p-value to have a result
        if p_value > required_p_value:
            result.inconclusive()
            return None

        # TODO Differentiate between decisive and indecisive
        if t_statistic > 0:
            result.decisive(1)
        else:
            result.decisive(2)
