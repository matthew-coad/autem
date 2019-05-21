from .specie_score_state import SpecieScoreState

class ScoreQuery:
    """
    Public queries related to scores and scoring
    """

    def __init__(self, container):
        self._container = container

    def get_container(self):
        return self._container

    def get_specie(self):
        return self.get_container().get_specie()

    # Splits

    def get_splits(self):
        """
        Nested array of the number of splits per repeat.

        Permits configurations like [[1,4],[5]] where
        we perform less splits at lower league levels.

        Each inner element represents a league level. So the above example has 3 league levels
        where we have two repeats of 5 splits at league level 3.
        """
        return SpecieScoreState.get(self.get_specie()).get_splits()

    def get_n_leagues(self):
        """
        Get the number of leagues
        """
        return sum(len(ls) for ls in self.get_splits())

    def get_n_repeats(self):
        """
        Get the number of fold repeats
        """
        return len(self.get_splits())

    def get_n_folds(self):
        """
        Get the number of folds
        """
        splits = self.get_splits()
        # Just use the first one
        return sum(splits[0])

    # Metric

    def get_metric(self):
        return SpecieScoreState.get(self.get_specie()).get_metric()

    # Folds

    def get_folds(self):
        return SpecieScoreState.get(self.get_specie()).get_folds()
