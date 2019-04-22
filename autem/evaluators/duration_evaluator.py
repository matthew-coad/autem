from .evaluator import Evaluater

import numpy as np
from scipy import stats

class DurationState:

    """
    Duration evaluation
    """
    def __init__(self):
        self.duration = None
        self.duration_std = None
        self.base_duration = None
        self.base_duration_std = None
        self.relative_duration = None

def get_duration_state(member):
    state = member.get_state("duration", lambda: DurationState())
    return state

class DurationEvaluator(Evaluater):
    """
    Assesses a members duration
    """

    def evaluate_member(self, member):
        super().evaluate_member(member)

        specie = member.get_specie()

        score_state = member.get_score_state()
        if not score_state.score_duration:
            return None

        candidates = [ m for m in specie.list_members() if m.id != member.id and m.league >= 1]
        if len(candidates) < 5:
            return None

        base_durations = []
        for candidate in candidates:
            base_durations.append(candidate.get_score_state().score_duration)

        duration_state = get_duration_state(member)
        duration_state.duration = score_state.score_duration
        duration_state.duration_std = score_state.score_duration_std
        duration_state.base_duration = np.mean(base_durations)
        duration_state.base_duration_std = np.std(base_durations)
        duration_state.relative_duration = duration_state.duration / duration_state.base_duration

    def record_member(self, member, record):
        super().record_member(member, record)

        duration_state = get_duration_state(member)
        record.DE_duration = duration_state.duration
        record.DE_duration_std = duration_state.duration_std
        record.DE_relative_duration = duration_state.relative_duration
