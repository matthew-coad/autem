class SimulationSettings:

    def __init__(self,
            components, properties, seed, 
            max_spotchecks, max_tunes, max_epochs, max_rounds, max_time, n_jobs, memory,
            max_reincarnations, max_population, max_league):
        self.components = components
        self.properties = properties
        self.seed = seed,
        self._max_spotchecks = max_spotchecks
        self._max_tunes = max_tunes
        self._max_epochs = max_epochs
        self._max_rounds = max_rounds
        self._max_time = max_time
        self._n_jobs = n_jobs
        self._memory = memory

        self._max_reincarnations = max_reincarnations
        self._max_population = max_population
        self._max_league = max_league

    def get_properties(self):
        return self.properties

    def get_components(self):
        return self.components

    def get_max_spotchecks(self):
        return self._max_spotchecks

    def get_max_tunes(self):
        return self._max_tunes

    def get_max_epochs(self):
        return self._max_epochs

    def get_max_rounds(self):
        return self._max_rounds

    def get_max_time(self):
        return self._max_time

    def get_max_reincarnations(self):
        return self._max_reincarnations

    def get_max_population(self):
        return self._max_population

    def get_max_league(self):
        return self._max_league

    def get_n_jobs(self):
        return self._n_jobs

    def get_memory(self):
        return self._memory

