from ..settings import Settings

class ScoreSettings(Settings):

    def __init__(self, container):
        Settings.__init__(self, container)

    def get_metric(self):
        return self.get_value("score_metric", lambda: None)

    def set_metric(self, metric):
        return self.set_value("score_metric", metric)

