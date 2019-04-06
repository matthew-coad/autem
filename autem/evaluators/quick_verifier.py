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
        base_duration = np.mean(verification_durations)
        score_duration = evaluation.score_duration
        standard_duration = score_duration / base_duration
        evaluation.base_duration = base_duration
        evaluation.standard_duration = standard_duration
        evaluation.long_duration = standard_duration > self.max_duration

        if evaluation.long_duration:
            member.kill()
            return None

    def evaluate_member(self, member):
        super().evaluate_member(member)

        evaluation = member.evaluation
        if hasattr(evaluation, "score_duration"):
            self.verify_member(member)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation

        if hasattr(evaluation, "base_duration"):
            record.QV_base_duation = evaluation.base_duration
            record.QV_standard_duration = evaluation.standard_duration
            record.QV_long_duration = 1 if evaluation.long_duration else 0
        else:
            record.QV_base_duation = None
            record.QV_standard_duration = None
            record.QV_long_duration = None
