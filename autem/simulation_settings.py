class SimulationSettings:

    def __init__(self,
            components, properties, seed, 
            max_specie, max_epochs, max_rounds, max_time, n_jobs,
            max_reincarnations, max_population, max_league):
        self.components = components
        self.properties = properties
        self.seed = seed,
        self.max_specie = max_specie
        self.max_epochs = max_epochs
        self.max_rounds = max_rounds
        self.max_time = max_time
        self.n_jobs = n_jobs

        self.max_reincarnations = max_reincarnations
        self.max_population = max_population
        self.max_league = max_league

    def get_properties(self):
        return self.properties

    def get_components(self):
        return self.components

    def get_hyper_parameters(self):
        hyper_parameters = [c for c in self.components if c.is_hyper_parameter() ]
        return hyper_parameters

    def get_controllers(self):
        controllers = [c for c in self.components if c.is_controller() ]
        return controllers

    def get_max_rounds(self):
        return self.max_rounds

    def get_max_population(self):
        return self.max_population

    def get_n_jobs(self):
        return self.n_jobs

