from .score_settings import ScoreSettings

class ScoreQuery:
    """
    Public queries related to scores and scoring
    """

    def __init__(self, container):
        self._container = container

    def get_container(self):
        return self._container

    def get_metric(self):
        return ScoreSettings(self.get_container()).get_metric()
