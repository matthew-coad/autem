from .component import Component
from .container import Container
from .scorers import ScorerContainer
from .loaders import LoaderContainer
from .ranking import Ranking

import time

from types import SimpleNamespace
import numpy as np

from .feedback import printProgressBar

class Epoch(Container, ScorerContainer, LoaderContainer):
    """
    Epoch of a simulation
    """
    def __init__(self, specie, epoch_id, epoch_n):

        Container.__init__(self)
        ScorerContainer.__init__(self)
        LoaderContainer.__init__(self)

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

    # Lifecycle

    def should_finish(self):
        """
        Should we finish the epoch?
        """
        max_epochs = self.get_settings().get_max_epochs()
        max_rounds = self.get_settings().get_max_rounds()
        max_time = self.get_settings().get_max_time()
        duration = time.time() - self.get_simulation().get_start_time()

        if max_time is not None and duration >= max_time:
            return (True, "Max time")

        if self.get_round() >= max_rounds:
            return (True, "Max rounds")
        
        return (False, None)

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

        for component in self.get_settings().get_controllers():
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
                for component in self.get_settings().get_controllers():
                    component.judge_epoch(self)

            # If we should finish the species, finish and bury all alive members
            # before we report
            finish_specie, reason = self.get_specie().should_finish()
            if finished and finish_specie:
                for member in self.list_members(alive=True):
                    member.finished(reason)
                    self.bury_member(member)

            # Report on what happened
            for member in report_members:
                self.record_member(member)

        self.report()

        self._end_time = time.time()
        self._alive = False

    def run_round(self):
        """
        Run a round of the simulation
        """

        self._round += 1

        specie = self.get_specie()
        mode = specie.get_mode()
        operation_name = "Evaluating %s specie %s mode %s epoch %s:" % (self._simulation.name, specie.id, mode, self.id)
        current_round = self.get_round()
        max_population = self.get_settings().get_max_population()
        max_rounds = self.get_settings().get_max_rounds()
        max_league = self.get_settings().get_max_league()

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
            self.evaluate_member(members[member_index])
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

    def get_alive(self):
        return self._alive

    def get_round(self):
        return self._round

    # Members

    def list_members(self, alive = None, top = None):
        return self.get_specie().list_members(alive = alive, top = top)

    def make_member(self, reason):        
        return self.get_specie().make_member(reason)

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        if not member.alive:
            raise RuntimeError("Member not alive")

        start_time = time.time()
        for component in self.get_settings().get_controllers():
            component.evaluate_member(member)
            if not member.alive:
                break
        duration = time.time() - start_time
        member.evaluated(duration)

    def contest_members(self, contestant1, contestant2):

        if contestant1.get_form() is contestant2.get_form():
            raise RuntimeError("Contestants have duplicate forms")

        if not contestant1.alive or not contestant2.alive:
            return None

        for component in self.get_settings().get_controllers():
            component.contest_members(contestant1, contestant2)

    def judge_member(self, member):
        for component in self.get_settings().get_controllers():
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

        for component in self.get_settings().get_controllers():
            component.rate_member(member)

    def rank_members(self):
        """
        Rank all members
        """
        inductees = self.list_members(alive = True, top = True)
        n_inductees = len(inductees)
        specie = self.get_specie()
        mode = specie.get_mode()
        progress_prefix = "Rating %s specie %s mode %s epoch %s:" % (self._simulation.name, specie.id, mode, self.id)
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

    # Reporting

    def record_member(self, member):
        """
        Generate a record on a member
        """
        self._simulation.reports.append(self._simulation.record_member(member))

    def report(self):
        """
        Report on progress of the simulation
        """
        self._simulation.report()

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

