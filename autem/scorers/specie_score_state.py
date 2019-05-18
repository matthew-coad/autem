class SpecieScoreState:
    """
    Scoring state needed at the specie level
    """

    def __init__(self):
        self._folds = None

    def get_folds(self):
        return self._folds

    def set_folds(self, folds):
        self._folds = folds

    def get(container):
        return container.get_state("specie_score", lambda: SpecieScoreState())
