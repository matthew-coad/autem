class DurationEvaluation:
    """
    Duration evaluation
    """
    def __init__(self, duration, duration_std, base_duration, base_duration_std, standard_duration):
        self.duration = duration
        self.duration_std = duration_std
        self.base_duration = base_duration
        self.base_duration_std = base_duration_std
        self.standard_duration = standard_duration
