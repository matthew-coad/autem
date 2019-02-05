from .loader import Loader

from ..simulators import Dataset
from ..simulators import Role

class Data(Loader):
    
    def __init__(self, name, x, y):
        Loader.__init__(self, name)
        self.x = x
        self.y = y

    def outline_simulation(self, simulation, outline):
        super().outline_simulation(simulation, outline)

        if not outline.has_attribute("data", Dataset.Battle):
            outline.append_attribute("data", Dataset.Battle, [ Role.Configuration ], self.name)
            outline.append_attribute("data", Dataset.Ranking, [ Role.Configuration ], self.name)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        super().record_member(member, record)
        if not self.is_active(member):
            return None
        record.data = self.name

    def record_ranking(self, member, record):
        super().record_ranking(member, record)
        if not self.is_active(member):
            return None
        record.data = self.name

    def load_divided(self):
        return (self.x, self.y)
