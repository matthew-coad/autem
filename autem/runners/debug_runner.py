from .runner import Runner

class DebugRunner(Runner):
    """
    Runner that runs the simulation in the local process.
    Useful when debugging. However does not support manual termination, but
    if your running in the debugger you don't need it!
    """

    def __init__(self, simulation):
        Runner.__init__(self, simulation)    

    def _run_internal(self):
        self.get_simulation()._run_internal()
