from .settings import Settings
import numpy as np

class SimulationSettings(Settings):
    """
    Provide access to the general simulation settings.
    """

    def __init__(self, container):
        Settings.__init__(self, container)

    def get_n_jobs(self):
        return self.get_value("n_jobs", lambda: -1)

    def set_n_jobs(self, n_jobs):
        return self.set_value("n_jobs", n_jobs)

    def get_memory(self):
        return self.get_value("memory", lambda: None)

    def set_memory(self, memory):
        return self.set_value("memory", memory)

    def get_seed(self):
        return self.get_value("seed", lambda: 1234)

    def set_seed(self, seed):
        return self.set_value("seed", seed)

    def get_random_state(self):
        return self.get_value("random_state", lambda: np.random.RandomState(self.get_seed()))

    def set_seed(self, seed):
        return self.set_value("seed", seed)

    def get_identity(self):
        return self.get_value("identity", lambda: {})

    def set_identity(self, identity):
        return self.set_value("identity", identity)

    def get_max_time(self):
        return self.get_value("max_time", lambda: None)

    def set_max_time(self, max_time):
        return self.set_value("max_time", max_time)

    def get_max_rounds(self):
        return self.get_value("max_rounds", lambda: 20)

    def set_max_rounds(self, max_rounds):
        return self.set_value("max_rounds", max_rounds)

    def get_max_population(self):
        return self.get_value("max_population", lambda: 20)

    def set_max_population(self, max_population):
        return self.set_value("max_population", max_population)

    def get_max_reincarnations(self):
        return self.get_value("max_reincarnations", lambda: 3)

    def set_max_reincarnations(self, max_reincarnations):
        return self.set_value("max_reincarnations", max_reincarnations)

    def get_max_epochs(self):
        return self.get_value("max_epochs", lambda: None)

    def set_max_epochs(self, max_epochs):
        return self.set_value("max_epochs", max_epochs)

    def get_max_league(self):
        # Not really changeable anymore, so read-only
        return self.get_value("max_league", lambda: 4) 

