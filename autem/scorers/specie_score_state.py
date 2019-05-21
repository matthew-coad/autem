class SpecieScoreState:
    """
    Scoring state needed at the specie level
    """

    def __init__(self):
        self._folds = None
        self._metric = None
        self._splits = None

    def get_splits(self):
        return self._splits

    def set_splits(self, splits):
        self._splits = splits

    def set_folds(self, folds):
        self._folds = folds

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
