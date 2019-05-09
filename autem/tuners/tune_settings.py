from ..settings import Settings

class TuneSettings(Settings):

    def __init__(self, container):
        Settings.__init__(self, container)

    def get_spotchecking(self):
        return self.get_value("spotchecking", lambda: None)

    def set_spotchecking(self, spotchecking):
        self.set_value("spotchecking", spotchecking)

    def get_tuning(self):
        return self.get_value("tuning", lambda: None)

    def set_tuning(self, tuning):
        self.set_value("tuning", tuning)
