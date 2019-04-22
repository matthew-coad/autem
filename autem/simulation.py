from .container import Container
from .workflows import Workflow, WorkflowContainer
from .lifecycle import LifecycleContainer
from .reporting import ReporterContainer, Dataset, Role, Outline
from .scorers import ScorerContainer
from .loaders import LoaderContainer

from .record import Record
from .member import Member
from .epoch import Epoch
from .specie import Specie
from .form import Form
from .ranking import Ranking
from .feedback import printProgressBar
from .choice import Choice
from .simulation_settings import SimulationSettings

import numpy
import time
import datetime

from types import SimpleNamespace

class Simulation(Container, LifecycleContainer, WorkflowContainer, ReporterContainer, ScorerContainer, LoaderContainer) :

    """Simulation state"""
    def __init__(self, name, components, properties = {}, n_jobs = -1, seed = 1234, memory = None):

        Container.__init__(self)
        LifecycleContainer.__init__(self)
        ReporterContainer.__init__(self)
        ScorerContainer.__init__(self)
        LoaderContainer.__init__(self) 

        self.name = name
        self._settings = SimulationSettings(properties = properties, memory = memory)

        self._raw_components = components
        self._components = None

        self.outline = None

        self._random_state = numpy.random.RandomState(seed)
        self._next_id = 1

        self._start_time = None
        self._end_time = None

        self._current_specie_id = None
        self._species = None
        self.reports = None

        self._n_jobs = n_jobs

    ## Core Environment

    def get_simulation(self):
        return self

    def get_settings(self):
        return self._settings

    def generate_id(self):
        id = self._next_id
        self._next_id += 1
        return id

    def get_random_state(self):
        """
        Get simulation loader
        """
        return self._random_state

    ## Properties

    def get_n_jobs(self):
        return self._n_jobs

    ## Components

    def _build_components(self):
        raw_components = self._raw_components
        components = []

        for component in raw_components:
            components.append(component)
            is_workflow = isinstance(component, Workflow)
            extensions = component.list_extensions(self) if is_workflow else []
            components.extend(extensions)
        self._components = components

    def list_components(self):
        if not self._components:
            raise RuntimeError("No components found")
        return self._components

    ## Species

    def list_species(self, alive = None, mode = None):
        """
        List species
        """
        def include_specie(specie):
            alive_passed = alive is None or specie.get_alive() == alive
            mode_passed = mode is None or specie.get_mode() == mode
            return alive_passed and mode_passed

        species = [ s for s in self._species.values() if include_specie(s) ]
        return species

    def get_current_specie(self):
        specie = self._species[self._current_specie_id] if self._current_specie_id else None
        return specie

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    ## Simulation life-cycle

    def should_finish(self):
        """
        Should we finish the simulation?
        """
        finish = None
        reason = None
        for workflow in self.list_workflows():
            finish, reason = workflow.is_simulation_finished(self)
            if not finish is None:
                break
        finish = finish if not finish is None else False
        return (finish, reason)

    def run(self):

        print("-----------------------------------------------------")
        today = datetime.datetime.now()
        print("Running %s - Started %s" % (self.name, today.strftime("%x %X")))

        self._start_time = time.time()
        self._current_specie_id = 0
        self._species = {}
        self.reports = []
        self._build_components()

        for component in self.list_workflows():
            component.configure_simulation(self)

        self.outline_simulation()
        for component in self.list_lifecycle_managers():
            component.start_simulation(self)

        finished = False
        while not finished:
            prior_specie = self.get_current_specie()
            next_epoch_id = prior_specie.get_current_epoch_id() + 1 if not prior_specie is None else 1
            next_specie_id = self._current_specie_id + 1
            n_specie = len(self.list_species())

            specie = Specie(self, next_specie_id, n_specie, next_epoch_id)
            self._species[specie.id] = specie
            self._current_specie_id = specie.id

            specie.run()
            finished, reason = self.should_finish()

        for component in self.list_lifecycle_managers():
            component.finish_simulation(self)

        self._end_time = time.time()
        duration = self.get_end_time() - self.get_start_time()
        print("%s - %s - Duration %s" % (self.name, reason, duration))

    def outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.get_settings().get_properties().keys():
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

        for component in self.list_reporters():
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

        prior_specie_rounds = sum(e.get_round() for s in self.list_species(alive = False) for e in s.list_epochs())
        prior_epoch_rounds = sum(e.get_round() for e in specie.list_epochs(alive = False) )
        step = prior_specie_rounds + prior_epoch_rounds + round

        record = Record()
        record.simulation = self.name
        properties = self.get_settings().get_properties()
        for property_key in properties.keys():
            setattr(record, property_key, properties[property_key])

        record.species = specie_id
        record.mode = specie.get_mode() 
        record.epoch = epoch_id
        record.round = round
        record.step = step
        record.member_id = member_id
        record.form_id = member.get_form().id
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

        for component in self.list_reporters():
            component.record_member(member, record)
        return record

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.list_reporters():
            component.report_simulation(self)
        self.reports = []
