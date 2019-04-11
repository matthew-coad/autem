from .member import Member
from .epoch import Epoch
from .specie import Specie
from .record import Record
from .dataset import Dataset
from .role import Role
from .outline import Outline
from .form import Form
from .ranking import Ranking
from types import SimpleNamespace
from .feedback import printProgressBar
from .maker import Maker
from .choice import Choice

import numpy
import time
import datetime

class Simulation:

    """Simulation state"""
    def __init__(self, name, components,
                seed = 1234, population_size = 10, top_league = 4,
                max_rounds = 20, max_reincarnations = 3, max_epochs = 10, max_time = None, n_jobs = -1, properties = {}):
        self.name = name
        self.components = components
        self.properties = properties
        self.population_size = population_size
        self.top_league = top_league
        self.max_rounds = max_rounds
        self.max_reincarnations = max_reincarnations
        self.max_epochs = max_epochs
        self.max_time = max_time
        self.n_jobs = n_jobs

        self.outline = None
        self.resources = SimpleNamespace()
        self.hyper_parameters = None
        self.controllers = None

        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1

        self.start_time = None
        self.end_time = None

        self.current_specie_id = None
        self.species = {}
        self.reports = []

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    ## Environment

    def get_current_specie(self):
        return self.species[self.current_specie_id]

    def get_simulation_resources(self):
        return self.resources

    def get_scorer(self):
        """
        Get simulation scorer
        """
        return self.get_simulation_resources().scorer

    def get_loader(self):
        """
        Get simulation loader
        """
        return self.get_simulation_resources().loader

    def get_random_state(self):
        """
        Get simulation loader
        """
        return self.random_state

    ## Simulation life-cycle

    def start(self):
        """
        Perform simulation startup
        """
        self.start_time = time.time()
        self.current_specie_id = 0
        self.hyper_parameters = [c for c in self.components if c.is_hyper_parameter() ]
        self.controllers = [c for c in self.components if c.is_controller() ]
        self.outline_simulation()
        for component in self.controllers:
            component.start_simulation(self)

    def should_finish(self):
        """
        Should we finish the simulation?
        """
        duration = time.time() - self.start_time
        epoch = self.get_current_specie().get_current_epoch()

        if not epoch.get_progressed():
            return (True, "No progress")

        if epoch.id == self.max_epochs:
            return (True, "Max epochs")

        if self.max_time is not None and duration >= self.max_time:
            return (True, "Max time")
        
        return (False, None)

    def run(self):

        print("-----------------------------------------------------")
        today = datetime.datetime.now()
        print("Running %s - Started %s" % (self.name, today.strftime("%x %X")))

        self.start()

        finished = False
        while not finished:
            specie = Specie(self, self.current_specie_id+1)
            self.species[specie.id] = specie
            self.current_specie_id = specie.id

            specie.run()
            finished, reason = self.should_finish()

        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print("%s - %s - Duration %s" % (self.name, reason, duration))

    def outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.properties.keys():
            outline.append_attribute(property_key, Dataset.Battle, [Role.Configuration])
        outline.append_attribute("species", Dataset.Battle, [Role.ID])
        outline.append_attribute("epoch", Dataset.Battle, [Role.ID])
        outline.append_attribute("round", Dataset.Battle, [Role.ID])
        outline.append_attribute("step", Dataset.Battle, [Role.ID])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("form_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("incarnation", Dataset.Battle, [Role.Property])
        outline.append_attribute("event", Dataset.Battle, [Role.Property])
        outline.append_attribute("fault", Dataset.Battle, [Role.Property])

        outline.append_attribute("ranking", Dataset.Battle, [ Role.KPI ])
        outline.append_attribute("incarnation_epoch", Dataset.Battle, [ Role.Property ])

        outline.append_attribute("league", Dataset.Battle, [Role.Property])
        outline.append_attribute("final", Dataset.Battle, [Role.Property])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def record_member(self, member):
        """
        Generate a record on a member
        """
        specie = self.get_current_specie()
        epoch = specie.get_current_epoch()
        member_id = member.id
        specie_id = specie.id
        epoch_id = epoch.id
        round = epoch.get_round()
        step = (epoch_id - 1) * epoch.get_max_rounds() + round

        record = Record()
        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])

        record.epoch = epoch_id
        record.species = specie_id
        record.round = round
        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation
        record.incarnation_epoch = member.incarnation_epoch_id
        record.event_time = time.ctime(member.evaluation_time)
        record.event = member.event
        record.event_reason = member.event_reason

        record.rating = member.rating
        record.rating_sd = member.rating_sd
        record.ranking = member.ranking

        record.league = member.league
        record.final = member.final

        for component in self.components:
            component.record_member(member, record)
        return record

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.controllers:
            component.report_simulation(self)
        self.reports = []
