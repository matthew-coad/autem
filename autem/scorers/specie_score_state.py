class SpecieScoreState:
    """
    Scoring state needed at the specie level
    """

    def __init__(self):
        self._folds = None
        self._metric = None

    def get_folds(self):
        return self._folds

    def set_folds(self, folds):
        self._folds = folds

    def get_metric(self):
        return self._metric

    def set_metric(self, metric):
        self._metric = metric

    def get(container):
        return container.get_state("specie_score", lambda: SpecieScoreState())
