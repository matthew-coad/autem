from ..simulators import Dataset, Role
from .battler import Battler

import numpy as np
from scipy import stats

class BestLearner(Battler):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        outline.append_attribute("t_statistic", Dataset.Battle, [Role.Measure], "t-statistic")
        outline.append_attribute("p_value", Dataset.Battle, [Role.Measure], "p value")

    def contest_members(self, contestant1, contestant2, outcome):

        # Make sure we define these extension values
        outcome.t_statistic = None
        outcome.p_value = None

        if outcome.is_conclusive():
            return None

        member1_scores = np.array([e.test_score for e in contestant1.evaluations])
        member2_scores = np.array([e.test_score for e in contestant2.evaluations])
        required_p_value = self.p_value

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            outcome.inconclusive()
            return None

        # Run the t-test
        test_result = stats.ttest_ind(member1_scores, member2_scores)
        outcome.t_statistic = test_result[0] # positive if 1 > 2
        outcome.p_value = test_result[1]

        # Need at least the required p-value to have am outcome
        if outcome.p_value > required_p_value:
            outcome.inconclusive()
            return None

        # TODO Differentiate between decisive and indecisive
        if outcome.t_statistic > 0:
            outcome.decisive(1)
        else:
            outcome.decisive(2)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        outcome = member.contests[-1] if member.contests else None
        record.t_statistic = outcome.t_statistic if outcome else None
        record.p_value = outcome.p_value if outcome else None
