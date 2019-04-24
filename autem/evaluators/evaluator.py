from ..simulation_manager import SimulationManager
from ..epoch_manager import EpochManager
from ..specie_manager import SpecieManager
from ..member_manager import MemberManager
from ..reporters import Reporter

class Evaluater(SimulationManager, SpecieManager, EpochManager, MemberManager, Reporter):

    def __init__(self):
        SimulationManager.__init__(self)
        SpecieManager.__init__(self)
        EpochManager.__init__(self)
        MemberManager.__init__(self)
        Reporter.__init__(self)
