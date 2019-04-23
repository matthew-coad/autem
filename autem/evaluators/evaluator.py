from ..simulation_manager import SimulationManager
from ..lifecycle import LifecycleManager
from ..reporting import Reporter

class Evaluater(SimulationManager, LifecycleManager, Reporter):

    def __init__(self):
        LifecycleManager.__init__(self)
        Reporter.__init__(self)
