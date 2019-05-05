from .container import Container
from .member_manager import MemberManagerContainer
from .hyper_parameter import HyperParameterContainer
from .preprocessors import PreprocessorContainer
from .learners import LearnerContainer
from .choice import Choice

from .component_state import ComponentState
from .simulation_settings import SimulationSettings

import time

from types import SimpleNamespace
import numpy as np
import copy

class Member(Container, MemberManagerContainer, HyperParameterContainer, PreprocessorContainer, LearnerContainer) :
    
    """
    Member of a population
    """
    def __init__(self, specie): 

        Container.__init__(self)
        MemberManagerContainer.__init__(self)
        HyperParameterContainer.__init__(self)
        PreprocessorContainer.__init__(self)
        LearnerContainer.__init__(self)

        self._specie = specie
        self.id = specie.generate_id()

        self.configuration = SimpleNamespace()

        self._form = None
        self._incarnation = 0
        self._incarnation_epoch_id = None

        self.event = None
        self.event_reason = None

        self.alive = 0
        self.final = 0

        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        self.evaluations = 0
        self.evaluation_time = None
        self.evaluation_duration = None

        self.wonlost = None

        self.league = 0

        self.ratings = SimpleNamespace()
        self.rating = None
        self.rating_sd = None

        self.ranking = None

    # Parameters

    def get_specie(self):
        return self._specie

    def get_simulation(self):
        return self.get_specie().get_simulation()

    def get_epoch(self):
        return self.get_specie().get_current_epoch()

    def get_parent(self):
        return self.get_epoch()

    # Configuration

    def get_form(self):
        return self._form

    def get_incarnation(self):
        return self._incarnation

    def get_incarnation_epoch_id(self):
        return self._incarnation_epoch_id

    # Decisions

    def get_decision(self):
        """
        Get the decision on the members choices
        """
        choices = ComponentState.get(self).list_choices()
        decision = tuple(c.get_active_component_name(self) for c in choices)
        return decision

    def set_decision(self, decision):
        """
        Set the decision on the members choices
        """
        choices = ComponentState.get(self).list_choices()
        for i, choice in enumerate(choices):
            choice.initialize_member(self)
            choice.force_member(self, decision[i])

    # Workflow

    def configure(self):
        """
        Configure the member
        """
        # Invoke managers in random order till one configures the member
        managers = self.list_member_managers()
        manager_indexes = SimulationSettings(self).get_random_state().choice(len(managers), size = len(managers), replace=False)
        configured, reason = (False, None)
        for index in manager_indexes:
            manager = managers[index]
            configured, reason = manager.configure_member(self)
            if not configured is None:
                break
        if configured is None:
            reason = "No configuration attempt"
        return (configured, reason)

    def prepare(self):
        """
        Prepare the members initial state
        """
        self.reset_state()
        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        managers = self.list_member_managers()
        prepared, reason = (True, None)
        for manager in managers:
            manager.prepare_member(self)
            if not self.fault is None:
                prepared, reason = (False, str(self.fault))
                break
        return (prepared, reason)

    def verify(self, max_reincarnations = 1, max_transmutations = 0):
        """
        Verify that a member has a valid configuration
        """
        form = self.get_specie().get_form(self.configuration)
        if form.incarnations > 0:
            return (False, "Currently incarnated")

        if form.reincarnations >= max_reincarnations:
            return (False, "Too many incarnations")

        return (True, None)

    def impersonate(self, other):
        """
        Impersonate an existing member
        """
        self.configuration = copy.deepcopy(other.configuration)

    def mutate(self, transmute):
        """
        Mutate the member, making a single random change to its configuration
        """
        prior_repr = repr(self.configuration)
        random_state = SimulationSettings(self).get_random_state()
        components = self.list_hyper_parameters()
        n_components = len(components)

        # Try each component in a random order until a component claims to have mutated the state
        component_indexes = random_state.choice(n_components, size=n_components, replace=False)
        for component_index in component_indexes:
            component = components[component_index]
            if not transmute:
                mutated = component.mutate_member(self)
            else:
                mutated = component.transmute_member(self)
            if mutated:
                if repr(self.configuration) == prior_repr:
                    raise RuntimeError("Configuration was not mutated as requested")
                return True
        return False

    def specialize(self, max_transmutations = 0):
        """
        Specialize the member so its valid, isn't incarnated more than once etc.
        """
        attempts = 0
        max_attempts = 100
        max_reincarnations = SimulationSettings(self).get_max_reincarnations()

        transmutations = 0
        specialized, reason = (False, None)
        while not specialized and attempts < max_attempts:
            attempts += 1

            prepared, reason = self.prepare()
            if prepared:
                specialized, reason = self.verify(max_reincarnations, max_transmutations)
            if not specialized:
                transmute = transmutations < max_transmutations
                self.mutate(transmute)
                transmutations = transmutations - 1 if transmute else transmutations

        return (specialized, reason)

    def incarnate(self, reason):
        """
        Incarnate a new prepared, configured, incarnated member
        """

        configured, fail_reason = self.configure()
        if not configured:
            return (False, fail_reason)

        self.alive = 1
        self.event = "birth"
        self.event_reason = reason
        self.evaluation_time = time.time()
        self.wonlost = []
        self.rating = None
        self.rating_sd = None
        self.ranking = None

        epoch = self.get_specie().get_current_epoch()
        form = self.get_specie().get_form(self.configuration)
        form.incarnate()
        self._form = form
        self._incarnation = form.reincarnations
        self._incarnation_epoch_id = epoch.id
        return (True, None)

    def prepare_epoch(self, epoch):
        self.event = None
        self.event_reason = None
        self.rating = None
        self.rating_sd = None
        self.ranking = None

    def prepare_round(self, round):
        self.event = "survive"
        self.event_reason = "Next round"
        self.evaluation_time = time.time()
        self.wonlost = []

    def evaluate(self):
        """
        Perform a round of member evaluation
        """
        if not self.alive:
            raise RuntimeError("Member not alive")

        self.evaluation_duration = None
        start_time = time.time()
        managers = self.list_member_managers()
        for manager in managers:
            manager.evaluate_member(self)
            if not self.alive:
                break
        duration = time.time() - start_time
        self.evaluation_duration = duration
        self.evaluations += 1

    def contest(self, other):

        if self.get_form() is other.get_form():
            raise RuntimeError("Contestants have duplicate forms")

        if not self.alive or not other.alive:
            return None

        managers = self.list_member_managers()
        for manager in managers:
            manager.contest_members(self, other)

    def judge(self):
        managers = self.list_member_managers()
        for manager in managers:
            manager.judge_member(self)

    def rate(self):
        """
        Rate a member
        """
        if not self.alive:
            raise RuntimeError("Member is not alive")

        managers = self.list_member_managers()
        for manager in managers:
            manager.rate_member(self)

    def kill(self, reason):
        """
        Kill this member
        """
        self.event = "death"
        self.event_reason = reason
        self.finish(reason)
        self.alive = 0
        self.final = 1

        managers = self.list_member_managers()
        for manager in managers:
            manager.finish_member(self)

    def fail(self, fault, operation, component):
        """
        Inform this member that it has failed for some reason
        """
        self.event = "fail"
        self.event_reason = str(fault)
        self.fault = fault
        self.fault_operation = operation
        self.fault_component = component
        self.fault_message = "%s %s - %s" % (operation, str(component), str(fault))
        self.alive = 0
        self.final = 1

        managers = self.list_member_managers()
        for manager in managers:
            manager.finish_member(self)

    def finish(self, reason):
        """
        Notify that this member it is finished with for some other reason, typically because the simulation has finished
        """
        self.event = "final"
        self.event_reason = reason
        self.alive = 0
        self.final = 1

        managers = self.list_member_managers()
        for manager in managers:
            manager.finish_member(self)

    def bury(self):
        """
        Bury this member, giving components a chance to clean up expensive resources
        """
        managers = self.list_member_managers()
        for manager in managers:
            manager.bury_member(self)
        self.get_form().disembody()

    # Notifications

    def victory(self):
        """
        Record a victory
        """
        self.wonlost.append(1)

    def defeat(self):
        """
        Record a defeat
        """
        self.wonlost.append(0)

    def promote(self, reason, league = None):
        """
        Promote the member to the next league
        """
        # When a member gets a promotion its wonlost record is erased
        self.event = "promotion"
        self.event_reason = reason
        if league is None:
            self.league += 1
        else:
            self.league = league

    def rated(self, rating, rating_sd):
        """
        Set the members rating in the hall of fame
        """
        self.rating = rating
        self.rating_sd = rating_sd

    def ranked(self,  ranking):
        """
        Set the members ranking in the hall of fame
        """
        self.ranking = ranking

