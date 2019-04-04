from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time
import warnings

class QuickVerifier(Evaluater):
    """
    Quick check that verifies if the score is anywhere near the ball-park.
    If the duration is substantially more than the durations of the top league members
    then drop it out
    """
    def __init__(self, max_duration = 3):
        self.max_duration = max_duration

    def verify_member(self, member):
        super().evaluate_member(member)

        simulation = member.simulation
        evaluation = member.evaluation

        candidates = [ m for m in simulation.members if m.id != member.id and m.league >= 1]
        if len(candidates) < 5:
            return None

        verification_durations = []
        for candidate in candidates:
            verification_durations.append(candidate.evaluation.score_duration)
        verification_duration = np.mean(verification_durations)
        score_duration = evaluation.score_duration
        standard_duration = score_duration / verification_duration

        if standard_duration > self.max_duration:
            evaluation.quick_verification = "%s too long" % (standard_duration)
            member.kill()
            return None
        evaluation.quick_verification = "%s" % (standard_duration)

    def evaluate_member(self, member):
        super().evaluate_member(member)

        evaluation = member.evaluation
        if not hasattr(evaluation, "quick_verification") and hasattr(evaluation, "score_duration"):
            self.verify_member(member)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "quick_verification"):
            record.quick_verification = evaluation.quick_verification
        else:
            record.quick_verification = None
