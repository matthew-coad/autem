from ..lifecycle import LifecycleManager
from ..reporting import Reporter

class Evaluater(LifecycleManager, Reporter):

    def __init__(self):
        LifecycleManager.__init__(self)
        Reporter.__init__(self)
