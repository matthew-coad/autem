from .container import Container
from .epoch_manager import EpochManagerContainer
from .hyper_parameter import HyperParameterContainer
from .ranking import Ranking

from .component_override import ComponentOverrideContainer
from .scorers import MemberLeagueState
from .simulation_settings import SimulationSettings

import time

from types import SimpleNamespace
import numpy as np

from .feedback import printProgressBar

class Epoch(Container, EpochManagerContainer, HyperParameterContainer, ComponentOverrideContainer):
    """
    Epoch of a simulation
    """
    def __init__(self, specie, epoch_id, epoch_n):

        Container.__init__(self)
        EpochManagerContainer.__init__(self)
        HyperParameterContainer.__init__(self)
        ComponentOverrideContainer.__init__(self)

        # Parameters
        self._specie = specie
        self._simulation = specie.get_simulation()
        self.id = epoch_id
        self._epoch_n = epoch_n
        self._name = str(epoch_id)

        # Initial State

        self._event = None
        self._event_reason = None

        self._start_time = None
        self._end_time = None

        self._alive = None
        self._round = None

        self._progressed = None
        self._ranking = None

    # Parameters

    def get_simulation(self):
        return self._simulation

    def get_specie(self):
        return self._specie

    def get_parent(self):
        return self.get_specie()

    def get_epoch_n(self):
        return self._epoch_n

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # State

    def get_alive(self):
        return self._alive

    def get_ranking(self):
        return self._ranking

    def get_prior_epoch(self):
        if self.get_epoch_n() == 1:
            return None
        prior_epoch_id = self.id - 1
        prior_epoch = self.get_specie().get_epoch(prior_epoch_id)
        return prior_epoch

    def get_round(self):
        return self._round

    # Workflow

    def should_finish(self):
        """
        Should we finish the epoch?
        """
        finish = None
        reason = None

        settings = SimulationSettings(self)
        if self.get_round() >= settings.get_max_rounds():
            return (True, "Max rounds")

        managers = self.list_epoch_managers()
        for manager in managers:
            finish, reason = manager.is_epoch_finished(self)
            if finish:
                break
        finish = finish if not finish is None else False
        return (finish, reason)

    def run(self):
        """
        Run an epoch
        """
        self._event = None
        self._event_reason = None

        self._alive = True
        self._start_time = time.time()
        self._round = 0

        self._progressed = None
        ranking = Ranking()
        ranking.inconclusive()
        self._ranking = ranking

        managers = self.list_epoch_managers()
        for manager in managers:
            manager.configure_epoch(self)

        for manager in managers:
            manager.prepare_epoch(self)

        members = self.list_members(alive = True)
        for member in members:
            member.prepare_epoch(self)

        finished = False
        while not finished:
            self.run_round()
            finished, reason = self.should_finish()

            report_members = self.list_members()

            # Bury dead members
            for member in self.list_members(alive = False):
                self.get_specie().bury_member(member)

            if finished:
                self.rank_members()
                for manager in managers:
                    manager.judge_epoch(self)

            # If we should finish the species, finish and bury all alive members
            # before we report
            if finished:
                finish_specie, reason = self.get_specie().should_finish()
                if finish_specie:
                    for member in self.list_members(alive=True):
                        member.finish(reason)
                        self.get_specie().bury_member(member)

            # Report on what happened
            for member in report_members:
                self.get_simulation().record_member(member)

        for manager in managers:
            manager.finish_epoch(self)

        self.get_simulation().report()

        for manager in managers:
            manager.bury_epoch(self)

        self._end_time = time.time()
        self._alive = False

    ## Round

    def run_round(self):
        """
        Run a round of the simulation
        """

        self._round += 1

        specie = self.get_specie()
        operation_name = "Evaluating %s specie %s epoch %s:" % (self.get_simulation().get_name(), specie.get_name(), self.get_name())
        current_round = self.get_round()
        settings = SimulationSettings(self)
        max_rounds = settings.get_max_rounds()
        max_population = settings.get_max_population()
        max_league = settings.get_max_league()

        # Prepare for the next round
        members = self.list_members(alive = True)
        for member in members:
            member.prepare_round(self.get_round())

        # Promote all living members
        for member in members:
            if member.league < max_league:
                member.promote("Survived")

        # Repopulate
        make_count = max_population - len(members)
        for make_index in range(make_count):
            self.get_specie().make_member("Population low")

        members = self.list_members(alive = True)

        # Ensure all members evaluated
        for member_index in range(len(members)):
            members[member_index].evaluate()
            printProgressBar(member_index + (current_round - 1) * max_population, max_rounds * max_population, prefix = operation_name, length = 50)

        # Have all evaluation survivors contest each other
        members = self.list_members(alive = True)
        for member1_index in range(len(members)-1):
            for member2_index in range(member1_index+1, len(members)):
                members[member1_index].contest(members[member2_index])

        # Judge all members
        for member in self.list_members():
            member.judge()

        printProgressBar(current_round * max_population, max_rounds * max_population, prefix = operation_name, length = 50)

    # Members

    def list_members(self, alive = None):
        return self.get_specie().list_members(alive = alive)

    def rank_members(self):
        """
        Rank all members
        """
        inductees = [ m for m in self.list_members(alive = True) if MemberLeagueState.get(m).is_veteran() ]
        n_inductees = len(inductees)
        specie = self.get_specie()
        progress_prefix = "Rating %s specie %s epoch %s:" % (self.get_simulation().get_name(), specie.get_name(), self.get_name())
        print("")
        if n_inductees > 0:
            for index in range(n_inductees):
                printProgressBar(index, n_inductees, prefix = progress_prefix, length = 50)
                inductees[index].rate()
            printProgressBar(n_inductees, n_inductees, prefix = progress_prefix, length = 50)

        candidates = [m for m in inductees if not m.rating is None]
        ranked_candidates = list(reversed(sorted(candidates, key=lambda member: member.rating)))
        rank = 1
        for candidate in ranked_candidates:
            candidate.ranked(rank)
            rank += 1

        ranking = Ranking()
        if not ranked_candidates:
            ranking.inconclusive()
        else:
            ranking.conclusive(ranked_candidates)

        self._ranking = ranking
        return ranking
