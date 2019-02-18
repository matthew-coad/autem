from ..simulators import Dataset, Role
from .contester import Contester

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class Peformance(Contester):
    """
    Establishes a preference for members that are quicker to evaluate
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        Contester.__init__(self, "PreferFast")
        self.p_value = p_value

    def contest_members(self, contestant1, contestant2, outcome):

        if not outcome.is_indecisive():
            return None

        required_p_value = self.p_value

        member1_scores = np.array(contestant1.durations)
        member2_scores = np.array(contestant2.durations)

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            return None

        # Run the t-test
        test_result = stats.ttest_ind(member1_scores, member2_scores)

        t_statistic = test_result[0] # positive if 1 > 2
        fastness = test_result[1]
        decisive = fastness < required_p_value / 2

        # Need at least the required p-value to have an outcome
        if fastness > required_p_value:
            return None

        # Determine the victor
        if t_statistic > 0:
            victor = 1
        else:
            victor = 2

        if victor == outcome.victor and decisive == outcome.is_decisive():
            return None

        if decisive:
            outcome.decisive(victor)
        else:
            outcome.indecisive(victor)
