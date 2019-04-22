from .container import Container
from .hyper_parameter import HyperParameterContainer
from .lifecycle import LifecycleContainer

from .member import Member
from .epoch import Epoch
from .form import Form
from .ranking import Ranking
from .choice import Choice
from .scorers import ScorerContainer
from .loaders import LoaderContainer


import numpy as np
import time
import datetime

from types import SimpleNamespace

class Specie(Container, LifecycleContainer, HyperParameterContainer, ScorerContainer, LoaderContainer):

    """
    Specie of a simulation
    """
    def __init__(self, simulation, specie_id, mode, specie_n, prior_epoch_id):

        Container.__init__(self)
        LifecycleContainer.__init__(self)
        HyperParameterContainer.__init__(self)
        ScorerContainer.__init__(self)
        LoaderContainer.__init__(self) 

        self._simulation = simulation
        self.id = specie_id
        self._mode = mode

        self._event = None
        self._event_reason = None

        self._start_time = None
        self._end_time = None

        self._alive = None

        self._specie_n = specie_n
        self._prior_epoch_id = prior_epoch_id
        self._current_epoch_id = None
        self._epochs = None

        self._members = None
        self._graveyard = None
        self._forms = None

    ## Context

    def get_simulation(self):
        return self._simulation

    # Properties
   
    def get_specie_n(self):
        return self._specie_n

    ## Mode

    def get_mode(self):
        return self._mode

    def is_spotchecking(self):
        return self.get_mode() == "spotcheck"

    def is_tuning(self):
        return self.get_mode() == "tune"

    ## Lifecycle

    def should_finish(self):
        """
        Should we finish the species?
        """
        epoch = self.get_current_epoch()
        duration = time.time() - self.get_simulation().get_start_time()
        n_epochs = len(self.list_epochs())
        max_epochs = self.get_settings().get_max_epochs()
        max_time = self.get_settings().get_max_time()

        if not epoch.get_progressed():
            return (True, "No progress")

        if n_epochs == max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)

    def run(self):
        """
        Run a specie
        """
        self._event = None
        self._event_reason = None

        self._alive = True
        self._start_time = time.time()

        self._current_epoch_id = self._prior_epoch_id
        self._epochs = {}

        self._members = []
        self._graveyard = []
        self._forms = {}

        for component in self.list_lifecycle_managers():
            component.start_specie(self)

        finished = False
        while not finished:
            n_epochs = len(self._epochs.values())
            epoch = Epoch(self, self._current_epoch_id+1, n_epochs + 1)
            self._epochs[epoch.id] = epoch
            self._current_epoch_id = epoch.id
            epoch.run()
            finished, reason = self.should_finish()

        for component in self.list_lifecycle_managers():
            component.judge_specie(self)

        self._end_time = time.time()
        self._alive = False

    def get_alive(self):
        return self._alive

    ## Epochs

    def get_current_epoch_id(self):
        return self._current_epoch_id

    def get_current_epoch(self):
        return self._epochs[self._current_epoch_id]

    def get_epoch(self, id):
        return self._epochs[id]

    def list_epochs(self, alive = None):
        """
        List epochs
        """
        def include_epoch(epochs):
            alive_passed = alive is None or epochs.get_alive() == alive
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

    def list_members(self, alive = None, top = None, buried = False):
        """
        List members
        """
        def include_member(member, is_buried):
            alive_passed = alive is None or member.alive == alive
            is_top = member.league == self.get_settings().get_max_league()
            top_passed = top is None or is_top == top
            buried_passed = buried is None or buried == is_buried
            return alive_passed and top_passed and buried_passed

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
        incarnated = member.incarnate(reason)
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

    ## Ranking

    def get_ranking(self):
        return self.get_current_epoch().get_ranking()
