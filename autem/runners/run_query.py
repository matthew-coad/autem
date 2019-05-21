from .run_state import RunState

import time

class RunQuery:
    """
    Public runtime state queries
    """

    def __init__(self, container):
        self._container = container

    def _get_run_state(self):
        return RunState.get(self._container.get_simulation())

    def get_start_time(self):
        return self._get_run_state().start_time

    def get_end_time(self):
        return self._get_run_state().end_time

    def get_max_time(self):
        return self._get_run_state().max_time

    def get_run_time(self):
        return time.time() - self.get_start_time()

    def is_timedout(self):
        return self.get_max_time() is not None and self.get_run_time() > self.get_max_time()

    def get_feedback(self):
        return self._get_run_state().feedback

    def was_escaped(self):
        """
        Was the run escaped?
        """
        return self._get_run_state().escaped
