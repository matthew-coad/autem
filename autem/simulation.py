from .container import Container
from .simulation_manager import SimulationManagerContainer
from .reporters import ReporterContainer, DataType, Role, Outline, Record
from .simulation_settings import SimulationSettings
from .specie import Specie
from .form import Form
from .ranking import Ranking
from .runners import RunQuery, DebugRunner

import numpy
import time
import datetime

from types import SimpleNamespace

class Simulation(Container, SimulationManagerContainer, ReporterContainer) :

    """Simulation state"""
    def __init__(self, name, components):

        Container.__init__(self)
        SimulationManagerContainer.__init__(self)
        ReporterContainer.__init__(self)

        self._name = name
        self._components = components

        self._next_id = 1

        self._start_time = None
        self._end_time = None

        self._current_specie_id = None
        self._species = {}
        self._records = []

        self._outline = None

        self._full_data = None
        self._training_data = None
        self._validation_data = None

    ## Properties

    def get_name(self):
        return self._name

    def get_simulation(self):
        return self

    def get_parent(self):
        return None

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

    ## Data

    def get_full_data(self):
        return self._full_data

    def set_full_data(self, full_data):
        self._full_data = full_data
        self._training_data = full_data
        self._validation_data = None

    def set_split_data(self, training_data, validation_data):
        self._training_data = training_data
        self._validation_data = validation_data

    def get_training_data(self):
        return self._training_data

    def get_validation_data(self):
        return self._validation_data

    ## Species

    def list_species(self, alive = None):
        """
        List species
        """
        def include_specie(specie):
            alive_passed = alive is None or specie.get_alive() == alive
            return alive_passed

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
        outline.append_attribute("simulation", DataType.Battle, [Role.Configuration])
        settings = SimulationSettings(self)
        for property_key in settings.get_identity().keys():
            outline.append_attribute(property_key, DataType.Battle, [Role.Configuration])
        outline.append_attribute("species", DataType.Battle, [Role.ID])
        outline.append_attribute("epoch", DataType.Battle, [Role.ID])
        outline.append_attribute("round", DataType.Battle, [Role.ID])
        outline.append_attribute("step", DataType.Battle, [Role.ID])
        outline.append_attribute("member_id", DataType.Battle, [Role.ID])
        outline.append_attribute("form_id", DataType.Battle, [Role.ID])
        outline.append_attribute("incarnation", DataType.Battle, [Role.Property])
        outline.append_attribute("event", DataType.Battle, [Role.Property])
        outline.append_attribute("fault", DataType.Battle, [Role.Property])

        outline.append_attribute("ranking", DataType.Battle, [ Role.KPI ])
        outline.append_attribute("incarnation_epoch", DataType.Battle, [ Role.Property ])

        outline.append_attribute("league", DataType.Battle, [Role.Property])
        outline.append_attribute("final", DataType.Battle, [Role.Property])

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

        settings = SimulationSettings(self)
        settings.set_random_state(numpy.random.RandomState(settings.get_seed()))

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

    def _run_internal(self):

        feedback = RunQuery(self).get_feedback()
        feedback.section(self.get_name())
        today = datetime.datetime.now()
        feedback.report("Started %s" % today.strftime("%x %X"))

        self._start_time = time.time()
        self._current_specie_id = 0

        configured, reason = self._configure()
        if not configured:
            feedback.report("Configuration failed - %s" % reason)
            return None

        outlined, reason = self._build_outline()
        if not outlined:
            feedback.report("Outline failed - %s" % reason)
            return None

        prepared, reason = self._prepare()
        if not prepared:
            feedback.report("Prepare failed - %s" % reason)
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
        feedback.report("%s - Duration %s" % (finish_reason, duration))

    def run(self):
        """
        Run the simulation.
        """
        runner = DebugRunner(self)
        runner.run()

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
        settings = SimulationSettings(self)

        prior_specie_rounds = sum(e.get_round() for s in self.list_species(alive = False) for e in s.list_epochs())
        prior_epoch_rounds = sum(e.get_round() for e in specie.list_epochs(alive = False) )
        step = prior_specie_rounds + prior_epoch_rounds + round

        record = Record()
        record.simulation = self.get_name()
        identity = settings.get_identity()
        for key in identity.keys():
            setattr(record, key, identity[key])

        record.species = specie_id
        record.epoch = epoch_id
        record.round = round
        record.step = step
        record.member_id = member_id
        record.form_id = member.get_form().id
        record.incarnation = member.get_incarnation()
        record.incarnation_epoch = member.get_incarnation_epoch_id()
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
