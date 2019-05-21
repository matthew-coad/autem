from .run_state import RunState
from .console_feedback import ConsoleFeedback

from .run_query import RunQuery

import time

class Runner:
    """
    Runners are responsible for "running" a simulation.

    They are responsible for setting up processes local or remote, providing feedback, allowing aborting,
    and recording the overall result.

    When the simulation itself is run they pass control to the runner
    """

    def __init__(self, simulation, max_time = None):
        self._simulation = simulation
        self._max_time = max_time

    def get_simulation(self):
        return self._simulation

    def get_feedback(self):
        return RunQuery(self.get_simulation()).get_feedback()

    def _run_internal(self):
        raise NotImplementedError()

    def run(self):
        """
        Required override that runs the simulation
        """
        run_state = RunState.get(self.get_simulation())
        run_state.start_time = time.time()
        run_state.max_time = self._max_time
        run_state.feedback = ConsoleFeedback()

        self._run_internal()
        run_state.end_time = time.time()
