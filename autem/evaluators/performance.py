from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class Peformance(Evaluater):
    """
    Establishes a preference for members that are quicker to evaluate
    Depends on the Accurancy component
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        Evaluater.__init__(self, "Performance")
        self.p_value = p_value

    # Performance evaluation is actually done by the accurancy component as
    # its done during the model fit.

    def contest_members(self, contestant1, contestant2, outcome):

        if not outcome.is_indecisive():
            return None

        required_p_value = self.p_value

        member1_accuracies = np.array(contestant1.durations)
        member2_accuracies = np.array(contestant2.durations)

        # Must have at least 3 scores each to make a comparison
        if len(member1_accuracies) < 3 or len(member2_accuracies) < 3:
            return None

        # Run the t-test
        test_result = stats.ttest_ind(member1_accuracies, member2_accuracies)

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

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "performance"):
            record.performance = evaluation.performance
        else:
            record.performance = None
