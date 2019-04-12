from .member import Member
from .epoch import Epoch
from .form import Form
from .ranking import Ranking
from .choice import Choice
from .maker import Maker


import numpy as np
import time
import datetime

from types import SimpleNamespace

class Specie:
    """
    Specie of a simulation
    """
    def __init__(self, simulation, specie_id): 
        self._simulation = simulation
        self.id = specie_id

        self._event = None
        self._event_reason = None

        self._start_time = None
        self._end_time = None

        self._alive = None
        self._resources = SimpleNamespace()

        self._current_epoch_id = None
        self._epochs = None

        self._members = None
        self._graveyard = None
        self._forms = None

        self._transmutation_rate = 0.5

    ## Environment

    def get_simulation(self):
        return self._simulation

    def get_settings(self):
        return self.get_simulation().get_settings()

    def get_current_epoch_id(self):
        return self._current_epoch_id

    def get_current_epoch(self):
        return self._epochs[self._current_epoch_id]

    def get_epoch(self, id):
        return self._epochs[id]

    def get_resources(self):
        return self._resources

    def get_max_reincarnations(self):
        return self.get_simulation().get_settings().max_reincarnations

    def get_max_epochs(self):
        return self.get_simulation().get_settings().max_epochs
    
    def get_max_time(self):
        return self.get_simulation().get_settings().max_time

    def get_max_league(self):
        return self.get_simulation().get_settings().max_league

    def get_n_jobs(self):
        return self.get_simulation().get_settings().n_jobs

    def get_random_state(self):
        return self.get_simulation().get_random_state()

    def get_scorer(self):
        return self.get_simulation().get_scorer()

    def get_loader(self):
        return self.get_simulation().get_loader()

    def generate_id(self):
        return self._simulation.generate_id()

    ## Lifecycle

    def should_finish(self):
        """
        Should we finish the species?
        """
        simulation = self._simulation
        epoch = self.get_current_epoch()
        duration = time.time() - simulation.start_time
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if not epoch.get_progressed():
            return (True, "No progress")

        if epoch.id == max_epochs:
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

        self._current_epoch_id = 0
        self._epochs = {}

        self._members = []
        self._graveyard = []
        self._forms = {}

        for component in self.get_settings().get_controllers():
            component.start_specie(self)

        finished = False
        while not finished:
            epoch = Epoch(self, self._current_epoch_id+1)
            self._epochs[epoch.id] = epoch
            self._current_epoch_id = epoch.id
            epoch.run()
            finished, reason = self.should_finish()

        for component in self.get_settings().get_controllers():
            component.judge_specie(self)

        self._end_time = time.time()
        self._alive = False

    ## Members

    def list_members(self, alive = None, top = None, graveyard = None):
        """
        List members
        """
        def include_member(member):
            alive_passed = alive is None or member.alive == alive
            is_top = member.league == self.get_max_league()
            top_passed = top is None or is_top == top
            return alive_passed and top_passed

        candidates = self._members
        if graveyard:
            candidates = candidates + self._graveyard
        members = [ m for m in candidates if include_member(m) ]
        return members

    def _mutate_member(self, member, transmute):
        """
        Mutate a member, making a guaranteed modification to its configuration
        """
        prior_repr = repr(member.configuration)
        random_state = self.get_random_state()
        components = self.get_settings().get_hyper_parameters()
        n_components = len(components)

        # Try each component in a random order until a component claims to have mutated the state
        component_indexes = random_state.choice(n_components, size=n_components, replace=False)
        for component_index in component_indexes:
            component = components[component_index]
            if not transmute:
                mutated = component.mutate_member(member)
            else:
                mutated = component.transmute_member(member)
            if mutated:
                if repr(member.configuration) == prior_repr:
                    raise RuntimeError("Configuration was not mutated as requested")
                return True
        return False

    def _prepare_member(self, member):
        """
        Perform once off member preparation
        """
        member.prepare()
        for component in self.get_settings().get_hyper_parameters():
            component.prepare_member(member)
            if not member.fault is None:
                break

    def specialize_member(self, member):
        """
        Make sure that the member has a new unique form
        """
        attempts = 0
        max_attempts = 100
        random_state = self.get_random_state()
        max_reincarnations = self.get_max_reincarnations()

        # Sometimes transmute the first mutation attept
        transmute = random_state.random_sample() <= self._transmutation_rate
        while True:
            self._prepare_member(member)
            if member.fault is None:
                form_key = repr(member.configuration)
                if not form_key in self._forms:
                    return True
                form = self._forms[form_key]
                if form.incarnations == 0 and form.reincarnations < max_reincarnations:
                    return True
            mutated = False
            if attempts == 0:
                mutated = self._mutate_member(member, transmute)
            else:
                mutated = self._mutate_member(member, False)
            if not mutated:
                return False

            attempts += 1
            if attempts > max_attempts:
                return False

    def make_member(self, reason):
        """
        Make a new member
        """

        # Find all makers
        makers = [ c for c in self.get_settings().get_components() if isinstance(c, Maker)]
        maker_indexes = self.get_random_state().choice(len(makers), size = len(makers), replace=False)

        # Invoke members in random order till one makes the member
        for maker_index in maker_indexes:
            member = makers[maker_index].make_member(self)
            if member:
                break
        if not member:
            raise RuntimeError("Member not created")
        form_key = repr(member.configuration)
        if form_key in self._forms:
            form = self._forms[form_key]
        else:
            form = Form(self.generate_id(), form_key)
            self._forms[form_key] = form
        form.incarnate()

        epoch = self.get_current_epoch()
        member.prepare_epoch(epoch)
        member.prepare_round(epoch, epoch.get_round())
        member.incarnated(epoch, form, form.reincarnations, reason)
        self._members.append(member)
        return member

    def bury_member(self, member):
        """
        Remove a member from the active pool
        """
        self._graveyard.append(member)
        self._members.remove(member)
        member.form.disembody()

