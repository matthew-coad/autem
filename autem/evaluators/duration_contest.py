from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score

class DurationContest(Evaluater):
    """
    Establishes a preference for members that are quicker to evaluate
    Depends on the AccurancyContest component
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    # Performance evaluation is actually done by the accurancy component as
    # its done during the model fit.

    def contest_members(self, contestant1, contestant2, outcome):

        required_p_value = self.p_value
        contestant1.evaluation.duration_contest = None
        contestant2.evaluation.duration_contest = None

        if not outcome.is_indecisive():
            return None

        if hasattr(contestant1.evaluation, "durations"):
            contestant1_scores = np.array(contestant1.evaluation.durations)
            contestant1_score = contestant1.evaluation.duration
        else:
            contestant1_scores = []
            contestant1_score = None

        if hasattr(contestant2.evaluation, "durations"):
            contestant2_scores = np.array(contestant2.evaluation.durations)
            contestant2_score = contestant2.evaluation.duration
        else:
            contestant2_scores = []
            contestant2_score = None

        # Record the durations each member has encountered so we can assess decisiveness in later contests
        if not contestant2_score is None:
            if not hasattr(contestant1.evaluation, "durations_encountered"):
                contestant1.evaluation.durations_encountered = []
            contestant1.evaluation.durations_encountered.append(contestant2_score)

        if not contestant1_score is None:
            if not hasattr(contestant2.evaluation, "durations_encountered"):
                contestant2.evaluation.durations_encountered = []
            contestant2.evaluation.durations_encountered.append(contestant1_score)

        # Must have at least 3 scores each to make a comparison
        if len(contestant1_scores) < 3 or len(contestant2_scores) < 3:
            outcome.inconclusive()
            return None

        # Run the t-test
        try:
            test_result = stats.ttest_ind(contestant1_scores, contestant2_scores)
        except:
            outcome.inconclusive()
            return None

        t_statistic = test_result[0] # positive if 1 > 2
        p_value = test_result[1]

        # Need at least the required p-value to have an outcome
        # But for a duration contest change the outcome
        if p_value > required_p_value:
            contestant1.evaluation.duration_contest = "Inconclusive"
            contestant2.evaluation.duration_contest = "Inconclusive"
            return None

        # Determine the victor. We want the duration to be low.
        if t_statistic < 0:
            victor = 1
        else:
            victor = 2

        victorious_contestant = contestant1 if victor == 1 else contestant2
        defeated_contestant = contestant2 if victor == 1 else contestant1

        # Determine decisiveness. A victory is decisive if its in the top half of the durations that each
        # member has encountered

        victorious_encounters = victorious_contestant.evaluation.durations_encountered
        defeated_encounters = defeated_contestant.evaluation.durations_encountered
        max_encounters = max(len(victorious_encounters), len(defeated_encounters))
        victorious_encounters = victorious_encounters[-max_encounters:]
        defeated_encounters = defeated_encounters[-max_encounters:]

        encounter_cutoff = defeated_contestant.evaluation.duration
        encounters = [ e for e in victorious_encounters + defeated_encounters if e >= encounter_cutoff ]
        decisive_cutoff = np.percentile(encounters, 55)
        decisive = victorious_contestant.evaluation.duration >= decisive_cutoff
        
        if decisive:
            victorious_contestant.evaluation.duration_contest = "Victory"
            defeated_contestant.evaluation.duration_contest = "Defeat"
            outcome.decisive(victor)
        else:
            victorious_contestant.evaluation.duration_contest = "Win"
            defeated_contestant.evaluation.duration_contest = "Loss"
            outcome.indecisive(victor)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "duration_contest"):
            record.duration_contest = evaluation.duration_contest
        else:
            record.duration_contest = None
