from .container import Container
from .specie_manager import SpecieManagerContainer
from .hyper_parameter import HyperParameterContainer
from .simulation_settings import SimulationSettings

from .member import Member
from .epoch import Epoch
from .form import Form
from .ranking import Ranking
from .choice import Choice

import numpy as np
import time
import datetime

from types import SimpleNamespace

class Specie(Container, SpecieManagerContainer, HyperParameterContainer):

    """
    Specie of a simulation
    """
    def __init__(self, simulation, specie_id, specie_n, next_epoch_id):

        Container.__init__(self)
        SpecieManagerContainer.__init__(self)
        HyperParameterContainer.__init__(self)

        self._simulation = simulation
        self.id = specie_id
        self._name = str(specie_id)
        self._specie_n = specie_n

        self._event = None
        self._event_reason = None

        self._start_time = None
        self._end_time = None
        self._alive = None

        self._next_epoch_id = next_epoch_id
        self._current_epoch_id = None
        self._epochs = {}

        self._members = []
        self._graveyard = []
        self._forms = {}

    ## Parameters

    def get_simulation(self):
        return self._simulation

    def get_specie(self):
        return self

    def get_parent(self):
        return self.get_simulation()

    def get_specie_n(self):
        return self._specie_n

    ## Configuration

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    ## State

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_alive(self):
        return self._alive

    def get_current_epoch_id(self):
        return self._current_epoch_id

    def get_current_epoch(self):
        return self._epochs[self._current_epoch_id]

    def get_epoch(self, id):
        return self._epochs[id]

    def get_ranking(self):
        return self.get_current_epoch().get_ranking()

    ## Lifecycle

    def should_finish(self):
        """
        Should we finish the species?
        """
        finish = None
        reason = None
        managers = self.list_specie_managers()
        for manager in managers:
            finish, reason = manager.is_specie_finished(self)
            if finish:
                break
        finish = finish if not finish is None else False
        return (finish, reason)

    def run(self):
        """
        Run a specie
        """
        self._event = None
        self._event_reason = None

        self._alive = True
        self._start_time = time.time()

        managers = self.list_specie_managers()
        for manager in managers:
            manager.configure_specie(self)

        for manager in managers:
            manager.prepare_specie(self)

        finished = False
        finish_reason = None
        while not finished:
            next_epoch_id = self._current_epoch_id + 1 if not self._current_epoch_id is None else self._next_epoch_id
            n_epochs = len(self._epochs.values())
            epoch = Epoch(self, next_epoch_id, n_epochs + 1)
            self._epochs[epoch.id] = epoch
            self._current_epoch_id = epoch.id
            epoch.run()
            finished, finish_reason = self.should_finish()

        for manager in managers:
            manager.judge_specie(self)

        for manager in managers:
            manager.finish_specie(self)

        for manager in managers:
            manager.bury_specie(self)

        self._end_time = time.time()
        self._alive = False
        duration = self.get_end_time() - self.get_start_time()
        print("Specie %s - %s - Duration %s" % (self.id, finish_reason, duration))

    ## Epochs

    def list_epochs(self, alive = None):
        """
        List epochs
        """
        def include_epoch(epoch):
            alive_passed = alive is None or epoch.get_alive() == alive
            return alive_passed

        epochs = [ e for e in self._epochs.values() if include_epoch(e) ]
        return epochs

    ## Forms

    def get_form(self, configuration):
        """
        Get form for a given configuration
        """
        form_key = repr(configuration)
        if form_key in self._forms:
            form = self._forms[form_key]
        else:
            form = Form(self.generate_id(), form_key)
            self._forms[form_key] = form
        return form

    ## Members

    def list_members(self, alive = None, buried = False):
        """
        List members
        """
        def include_member(member, is_buried):
            alive_passed = alive is None or member.alive == alive
            buried_passed = buried is None or buried == is_buried
            return alive_passed and buried_passed

        members = [ m for m in self._members if include_member(m, False) ]
        if buried is None or buried:
            buried_members = [ m for m in self._graveyard if include_member(m, True) ]
            members = members + buried_members
        return members

    def make_member(self, reason):
        """
        Make a new member
        """
        member = Member(self)
        incarnated, reason = member.incarnate(reason)
        if not incarnated:
            return None
        self._members.append(member)
        return member

    def bury_member(self, member):
        """
        Remove a member from the active pool
        """
        member.bury()
        self._graveyard.append(member)
        self._members.remove(member)
