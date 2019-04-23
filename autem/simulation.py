from .container import Container
from .simulation_manager import SimulationManagerContainer
from .reporting import ReporterContainer, Dataset, Role, Outline

from .record import Record
from .member import Member
from .epoch import Epoch
from .specie import Specie
from .form import Form
from .ranking import Ranking
from .feedback import printProgressBar
from .choice import Choice

import numpy
import time
import datetime

from types import SimpleNamespace

class Simulation(Container, SimulationManagerContainer, ReporterContainer) :

    """Simulation state"""
    def __init__(self, name, components, identity = {}, n_jobs = -1, seed = 1234, memory = None):

        Container.__init__(self)
        SimulationManagerContainer.__init__(self)
        ReporterContainer.__init__(self)

        self._name = name
        self._components = components
        self._identity = identity
        self._n_jobs = n_jobs
        self._seed = seed
        self._memory = memory

        self._random_state = numpy.random.RandomState(seed)
        self._next_id = 1

        self._start_time = None
        self._end_time = None

        self._current_specie_id = None
        self._species = {}
        self._records = []

        self._outline = None

        self._loader = None
        self._scorer = None

    ## Properties

    def get_name(self):
        return self._name

    def get_simulation(self):
        return self

    def get_random_state(self):
        return self._random_state

    def get_n_jobs(self):
        return self._n_jobs

    def get_seed(self):
        return self._seed

    def get_memory(self):
        return self._memory

    def get_identity(self):
        return self._identity

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    ## Ids

    def generate_id(self):
        id = self._next_id
        self._next_id += 1
        return id

    ## Components

    def list_components(self):
        if not self._components:
            raise RuntimeError("No components found")
        return self._components[:]

    def set_components(self, components):
        self._components = components

    ## Scorers

    def get_scorer(self):
        return self._scorer

    def set_scorer(self, scorer):
        self._scorer = scorer

    ## Loader

    def get_loader(self):
        return self._loader

    def set_loader(self, loader):
        self._loader = loader

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

    ## Outline

    def _build_outline(self):
        """
        Build the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.get_identity().keys():
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
        self._outline = outline
        return (True, None)

    def get_outline(self):
        return self._outline

    ## Simulation life-cycle

    def _configure(self):
        """
        Perform simulation configuration.
        """
        components = self.list_simulation_managers()
        for component in components:
            component.configure_simulation(self)
        return (True, None)

    def _prepare(self):
        """
        Perform simulation preparation.
        """
        components = self.list_simulation_managers()
        for component in components:
            component.prepare_simulation(self)
        return (True, None)

    def _should_finish(self):
        """
        Should we finish the simulation?
        """
        finish = None
        reason = None
        for component in self.list_simulation_managers():
            finish, reason = component.is_simulation_finished(self)
            if finish:
                break
        finish = finish if not finish is None else False
        return (finish, reason)

    def _finish(self):
        """
        Perform final tasks.
        """
        components = self.list_simulation_managers()
        for component in components:
            component.finish_simulation(self)

    def _bury(self):
        """
        Bury any expensive resources
        """
        components = self.list_simulation_managers()
        for component in components:
            component.bury_simulation(self)

    def run(self):

        print("-----------------------------------------------------")
        today = datetime.datetime.now()
        print("Running %s - Started %s" % (self.get_name(), today.strftime("%x %X")))

        self._start_time = time.time()
        self._current_specie_id = 0

        configured, reason = self._configure()
        if not configured:
            print("%s - configuration failed - %s" % (self.get_name(), reason))
            return None

        outlined, reason = self._build_outline()
        if not outlined:
            print("%s - outline failed - %s" % (self.get_name(), reason))
            return None

        prepared, reason = self._prepare()
        if not prepared:
            print("%s - prepare failed - %s" % (self.get_name(), reason))
            return None

        should_finish, finish_reason = self._should_finish()
        while not should_finish:
            prior_specie = self.get_current_specie()
            next_epoch_id = prior_specie.get_current_epoch_id() + 1 if not prior_specie is None else 1
            next_specie_id = self._current_specie_id + 1
            n_specie = len(self.list_species())

            specie = Specie(self, next_specie_id, n_specie, next_epoch_id)
            self._species[specie.id] = specie
            self._current_specie_id = specie.id
            specie.run()
            should_finish, finish_reason = self._should_finish()

        self._finish()
        self._bury()

        self._end_time = time.time()
        duration = self.get_end_time() - self.get_start_time()
        print("%s - %s - Duration %s" % (self.get_name(), finish_reason, duration))

    ## Reporting

    def get_records(self):
        return self._records

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
        record.simulation = self.get_name()
        identity = self.get_identity()
        for key in identity.keys():
            setattr(record, key, identity[key])

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
       
        self._records.append(record)
        return record

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.list_reporters():
            component.report_simulation(self)
        self._records = []
