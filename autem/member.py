from .container import Container
from .lifecycle import LifecycleManager
from .hyper_parameter import HyperParameterContainer
from .scorers import ScorerContainer
from .loaders import LoaderContainer
from .preprocessors import PreprocessorContainer
from .learners import LearnerContainer
from .evaluators.score_evaluator import ScoreContainer

from .maker import Maker


import time

from types import SimpleNamespace
import numpy as np
import copy

class Member(Container, LifecycleManager, HyperParameterContainer, ScorerContainer, LoaderContainer, PreprocessorContainer, LearnerContainer, ScoreContainer) :
    """
    Member of a population
    """
    def __init__(self, specie): 

        Container.__init__(self)
        LifecycleManager.__init__(self)
        HyperParameterContainer.__init__(self)
        ScorerContainer.__init__(self)
        LoaderContainer.__init__(self)
        PreprocessorContainer.__init__(self)
        LearnerContainer.__init__(self)
        ScoreContainer.__init__(self)

        self._specie = specie

        self.id = specie.generate_id()
        self.configuration = SimpleNamespace()
        self.form = None
        self.incarnation = 0
        self.incarnation_epoch_id = None

        self.event = None
        self.event_reason = None

        self.alive = 0
        self.final = 0

        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        self.evaluation = SimpleNamespace()
        self.evaluations = 0
        self.evaluation_time = None
        self.evaluation_duration = None

        self.wonlost = None # Map of wonlost record per epoch

        self.league = 0

        self.ratings = SimpleNamespace()
        self.rating = None
        self.rating_sd = None

        self.ranking = None

    # Context

    def get_specie(self):
        return self._specie

    def get_simulation(self):
        return self.get_specie().get_simulation()

    # Evaluations

    def get_evaluations(self):
        return self.evaluation

    def get_evaluation(self, name, default = lambda: None):
        if not hasattr(self.evaluation, name):
            setattr(self.evaluation, name, default())
        return getattr(self.evaluation, name)

    def set_evaluation(self, name, value):
        setattr(self.evaluation, name, value)


    # Forms

    def get_form(self):
        """
        Get this members form
        """
        return self.form

    # Preparation

    def prepare(self):
        """
        Perform pre-incarnation preparation
        """
        self.reset_state()
        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        for component in self.list_hyper_parameters():
            component.prepare_member(self)
            if not self.fault is None:
                break

    def impersonate(self, other):
        """
        Impersonate an existing member
        """
        self.configuration = copy.deepcopy(other.configuration)

    def mutate(self, transmute):
        """
        Mutate the member
        """
        prior_repr = repr(self.configuration)
        random_state = self.get_random_state()
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

    def get_transmutation_rate(self):
        return 0.0

    def specialize(self):
        """
        Make sure that the member has a new unique form
        """
        attempts = 0
        max_attempts = 100
        max_reincarnations = self.get_settings().get_max_reincarnations()

        # Sometimes transmute the first mutation attept
        transmute = self.get_random_state().random_sample() <= self.get_transmutation_rate()
        while True:
            self.prepare()
            if self.fault is None:
                form = self.get_specie().get_form(self.configuration)
                if form.incarnations == 0 and form.reincarnations < max_reincarnations:
                    return True
            mutated = False
            mutated = self.mutate(transmute)
            transmute = False
            attempts += 1
            if attempts > max_attempts:
                return False

    def incarnate(self, reason):
        """
        Incarnate a new form
        """

        # Find all makers
        makers = [ c for c in self.get_settings().get_components() if isinstance(c, Maker)]
        maker_indexes = self.get_random_state().choice(len(makers), size = len(makers), replace=False)

        # Invoke members in random order till one makes the member
        configured = False
        for maker_index in maker_indexes:
            configured = makers[maker_index].configure_member(self)
            if configured:
                break

        if not configured:
            raise RuntimeError("Member not configured")

        specialized = self.specialize()
        if not specialized:
            return False

        self.alive = 1
        self.event = "birth"
        self.event_reason = reason
        self.evaluation_time = time.time()
        self.wonlost = []
        self.rating = None
        self.rating_sd = None
        self.ranking = None

        epoch = self.get_specie().get_current_epoch()
        self.incarnation_epoch_id = epoch.id

        form = self.get_specie().get_form(self.configuration)
        form.incarnate()
        self.form = form
        self.incarnation = form.reincarnations
        return True

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

    def evaluated(self, duration):
        self.evaluation_duration = duration
        self.evaluations += 1

    def victory(self):
        """
        Record a victory at a given step
        """
        self.wonlost.append(1)

    def defeat(self):
        """
        Record a defeat at a given epoch
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

    def kill(self, reason):
        """
        Kill this member
        """
        self.event = "death"
        self.event_reason = reason
        self.alive = 0
        self.final = 1

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

    def finished(self, reason):
        """
        Notify that this member it is finished with, because the simulation has finished
        """
        self.event = "final"
        self.event_reason = reason
        self.alive = 0
        self.final = 1

    def buried(self):
        """
        Change this member to the buried state
        """
        self.form.disembody()

