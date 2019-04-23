from .container import Container
from .workflows import WorkflowContainer
from .lifecycle import LifecycleContainer
from .hyper_parameter import HyperParameterContainer
from .ranking import Ranking

import time

from types import SimpleNamespace
import numpy as np

from .feedback import printProgressBar

class Epoch(Container, WorkflowContainer, LifecycleContainer, HyperParameterContainer):
    """
    Epoch of a simulation
    """
    def __init__(self, specie, epoch_id, epoch_n):

        self._specie = specie
        self._simulation = specie.get_simulation()

        self.id = epoch_id
        self._epoch_n = epoch_n

        self._event = None
        self._event_reason = None

        self._start_time = None
        self._end_time = None

        self._alive = None
        self._round = None

        self._progressed = None
        self._ranking = None

        self._max_rounds = None

    # Context

    def get_simulation(self):
        return self._simulation

    def get_specie(self):
        return self._specie

    def get_epoch_n(self):
        """
        Epoch number. Number of the epoch within the specie
        """
        return self._epoch_n

    # Configuration

    def get_max_rounds(self):
        return self._max_rounds

    def set_max_rounds(self, max_rounds):
        self._max_rounds = max_rounds

    # Lifecycle

    def get_alive(self):
        return self._alive

    def should_finish(self):
        """
        Should we finish the epoch?
        """
        finish = None
        reason = None

        if self.get_round() >= self.get_max_rounds():
            return (True, "Max rounds")

        workflows = self.list_workflows()
        for workflow in workflows:
            finish, reason = workflow.is_epoch_finished(self)
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

        for workflow in self.list_workflows():
            workflow.configure_epoch(self)

        for component in self.list_lifecycle_managers():
            component.start_epoch(self)

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
                self.bury_member(member)

            if finished:
                self.rank_members()
                for component in self.list_lifecycle_managers():
                    component.judge_epoch(self)

            # If we should finish the species, finish and bury all alive members
            # before we report
            if finished:
                finish_specie, reason = self.get_specie().should_finish()
                if finish_specie:
                    for member in self.list_members(alive=True):
                        member.finished(reason)
                        self.bury_member(member)

            # Report on what happened
            for member in report_members:
                self.get_simulation().record_member(member)

        self.get_simulation().report()

        self._end_time = time.time()
        self._alive = False

    ## Round

    def get_round(self):
        return self._round

    def run_round(self):
        """
        Run a round of the simulation
        """

        self._round += 1

        specie = self.get_specie()
        mode = specie.get_mode()
        operation_name = "Evaluating %s specie %s mode %s epoch %s:" % (self.get_simulation().get_name(), specie.id, mode, self.id)
        current_round = self.get_round()
        max_rounds = self.get_max_rounds()
        max_population = specie.get_max_population()
        max_league = specie.get_max_league()

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
            self.make_member("Population low")

        members = self.list_members(alive = True)

        # Ensure all members evaluated
        for member_index in range(len(members)):
            members[member_index].evaluate()
            printProgressBar(member_index + (current_round - 1) * max_population, max_rounds * max_population, prefix = operation_name, length = 50)

        # Have all evaluation survivors contest each other
        members = self.list_members(alive = True)
        for member1_index in range(len(members)-1):
            for member2_index in range(member1_index+1, len(members)):
                self.contest_members(members[member1_index], members[member2_index])

        # Judge all members
        for member in self.list_members():
            self.judge_member(member)

        printProgressBar(current_round * max_population, max_rounds * max_population, prefix = operation_name, length = 50)

    # Members

    def list_members(self, alive = None, top = None):
        return self.get_specie().list_members(alive = alive, top = top)

    def make_member(self, reason):        
        return self.get_specie().make_member(reason)

    def contest_members(self, contestant1, contestant2):

        if contestant1.get_form() is contestant2.get_form():
            raise RuntimeError("Contestants have duplicate forms")

        if not contestant1.alive or not contestant2.alive:
            return None

        for component in self.list_lifecycle_managers():
            component.contest_members(contestant1, contestant2)

    def judge_member(self, member):
        for component in self.list_lifecycle_managers():
            component.judge_member(member)

    def bury_member(self, member):
        """
        Remove a member from the active pool
        """
        self.get_specie().bury_member(member)

    def rate_member(self, member):
        """
        Rate a member
        """
        if not member.alive:
            raise RuntimeError("Members is not alive")

        for component in self.list_lifecycle_managers():
            component.rate_member(member)

    def rank_members(self):
        """
        Rank all members
        """
        inductees = self.list_members(alive = True, top = True)
        n_inductees = len(inductees)
        specie = self.get_specie()
        mode = specie.get_mode()
        progress_prefix = "Rating %s specie %s mode %s epoch %s:" % (self.get_simulation().get_name(), specie.id, mode, self.id)
        print("")
        if n_inductees > 0:
            for index in range(n_inductees):
                printProgressBar(index, n_inductees, prefix = progress_prefix, length = 50)
                self.rate_member(inductees[index])
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

    def get_ranking(self):
        return self._ranking

    # Progress

    def progress(self, progressed, reason):
        """
        Inform the epoch of its progress
        """
        # When a member gets a promotion its wonlost record is erased
        self._progressed = progressed
        self._event = "progress"
        self._event_reason = reason

    def get_progressed(self):
        return self._progressed

