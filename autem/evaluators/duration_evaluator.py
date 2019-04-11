from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from .duration_evaluation import DurationEvaluation

class DurationEvaluator(Evaluater):
    """
    Assesses a members duration
    """

    def get_score_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "score_evaluation"):
            evaluation.score_evaluation = ScoreEvaluation()
        return evaluation.score_evaluation

    def get_duration_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "duration_evaluation"):
            evaluation.duration_evaluation = DurationEvaluation()
        return evaluation.duration_evaluation

    def evaluate_member(self, member):
        super().evaluate_member(member)

        specie = member.get_specie()

        score_evaluation = self.get_score_evaluation(member)
        if not score_evaluation.score_duration:
            return None

        candidates = [ m for m in specie.list_members() if m.id != member.id and m.league >= 1]
        if len(candidates) < 5:
            return None

        base_durations = []
        for candidate in candidates:
            base_durations.append(self.get_score_evaluation(candidate).score_duration)

        duration_evaluation = self.get_duration_evaluation(member)

        duration_evaluation.duration = score_evaluation.score_duration
        duration_evaluation.duration_std = score_evaluation.score_duration_std
        duration_evaluation.base_duration = np.mean(base_durations)
        duration_evaluation.base_duration_std = np.std(base_durations)
        duration_evaluation.relative_duration = duration_evaluation.duration / duration_evaluation.base_duration

    def record_member(self, member, record):
        super().record_member(member, record)

        duration_evaluation = self.get_duration_evaluation(member)
        record.DE_duration = duration_evaluation.duration
        record.DE_duration_std = duration_evaluation.duration_std
        record.DE_relative_duration = duration_evaluation.relative_duration
