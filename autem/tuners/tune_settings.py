from ..settings import Settings

class TuneSettings(Settings):

    def __init__(self, container):
        Settings.__init__(container)

    def get_tuning(self):
        return self.get_value("tuning", lambda: None)

    def set_tuning(self, tuning):
        self.set_value("tuning", tuning)
