from .reporter import Reporter

class ReporterContainer:

    """
    MixIn that adds reporting support to containers
    """

    def list_reporters(self):
        managers = [c for c in self.list_components() if isinstance(c, Reporter) ]
        return managers
