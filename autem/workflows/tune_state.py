class TuneState:

    def __init__(self):
        self._tuning = False
        self._prototype = None

    def get_tuning(self):
        return self._tuning

    def set_tuning(self, tuning):
        self._tuning = tuning

    def get_prototype(self):
        return self._prototype

    def set_prototype(self, prototype):
        self._prototype = prototype

    def get(container):
        return container.get_state("Tune", lambda: TuneState())
