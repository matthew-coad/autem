from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from .duration_evaluation import DurationEvaluation

class DurationEvaluator(Evaluater):
    """
    Assesses a members duration
    """

    def evaluate_member(self, member):
        super().evaluate_member(member)

        simulation = member.simulation
        evaluation = member.evaluation

        if not hasattr(evaluation, "score_duration"):
            return None

        candidates = [ m for m in simulation.members if m.id != member.id and m.league >= 1]
        if len(candidates) < 5:
            return None

        base_durations = []
        for candidate in candidates:
            base_durations.append(candidate.evaluation.score_duration)

        duration = evaluation.score_duration
        duration_std = evaluation.score_duration_std
        base_duration = np.mean(base_durations)
        base_duration_std = np.std(base_durations)
        standard_duration = duration / base_duration

        evaluation.duration_evaluation = DurationEvaluation(duration, duration_std, base_duration, base_duration_std, standard_duration)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        duration_evaluation = evaluation.duration_evaluation if hasattr(evaluation, "duration_evaluation") else None

        if duration_evaluation:
            record.DE_duration = duration_evaluation.duration
            record.DE_duration_std = duration_evaluation.duration_std
            record.DE_base_duration = duration_evaluation.base_duration
            record.DE_base_duration_std = duration_evaluation.base_duration_std
            record.DE_standard_duration = duration_evaluation.standard_duration
        else:
            record.DE_duration = None
            record.DE_duration_std = None
            record.DE_base_duration = None
            record.DE_base_duration_std = None
            record.DE_standard_duration = None
