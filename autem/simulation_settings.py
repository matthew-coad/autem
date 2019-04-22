class SimulationSettings:

    def __init__(self, properties,  memory):
        self.properties = properties
        self._memory = memory

    def get_properties(self):
        return self.properties

    def get_memory(self):
        return self._memory

