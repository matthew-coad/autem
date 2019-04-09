from .member import Member
from .record import Record
from .dataset import Dataset
from .role import Role
from .outline import Outline
from .form import Form
from .ranking import Ranking
from types import SimpleNamespace
from .feedback import printProgressBar
from .maker import Maker
from .choice import Choice

import numpy
import time
import datetime

class Simulation:

    """Simulation state"""
    def __init__(self, name, components, seed = 1234, population_size = 10, top_league = 4, max_reincarnations = 3, properties = {}, n_jobs = -1):
        self.name = name
        self.components = components
        self.properties = properties
        self.population_size = population_size
        self.top_league = top_league
        self.max_reincarnations = max_reincarnations
        self.n_jobs = n_jobs
        self.transmutation_rate = 0.5

        self.outline = None
        self.resources = SimpleNamespace()
        self.hyper_parameters = None
        self.controllers = None

        self.epochs = None
        self.rounds = None

        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1
        self.epoch = None
        self.round = None
        self.step = None
        self.running = False

        self.members = []
        self.graveyard = []
        self.forms = {}
        self.ranking = None
        self.reports = []

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def list_members(self, alive = None):
        """
        List members
        """
        def include_member(member):
            alive_passed = alive is None or member.alive == alive
            return alive_passed

        candidates = self.members
        members = [ m for m in candidates if include_member(m) ]
        return members

    def mutate_member(self, member, transmute):
        """
        Mutate a member, making a guaranteed modification to its configuration
        """
        prior_repr = repr(member.configuration)
        random_state = self.random_state
        components = self.hyper_parameters
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

    def specialize_member(self, member):
        """
        Make sure that the member has a new unique form
        """
        attempts = 0
        max_attempts = 100
        random_state = self.random_state
        max_reincarnations = self.max_reincarnations

        # Sometimes transmute the first mutation attept
        transmute = random_state.random_sample() <= self.transmutation_rate
        while True:
            self.prepare_member(member)
            if member.fault is None:
                form_key = repr(member.configuration)
                if not form_key in self.forms:
                    return True
                form = self.forms[form_key]
                if form.incarnations == 0 and form.reincarnations < max_reincarnations:
                    return True
            mutated = False
            if attempts == 0:
                mutated = self.mutate_member(member, transmute)
            else:
                mutated = self.mutate_member(member, False)
            if not mutated:
                return False

            attempts += 1
            if attempts > max_attempts:
                return False

    def prepare_member(self, member):
        """
        Perform once off member preparation
        """
        member.prepare()
        for component in self.hyper_parameters:
            component.prepare_member(member)
            if not member.fault is None:
                break

    def make_member(self):
        """
        Make a new member
        """

        # Find all makers
        makers = [ c for c in self.components if isinstance(c, Maker)]
        maker_indexes = self.random_state.choice(len(makers), size = len(makers), replace=False)

        # Invoke members in random order till one makes the member
        for maker_index in maker_indexes:
            member = makers[maker_index].make_member(self)
            if member:
                break
        if not member:
            raise RuntimeError("Member not created")
        form_key = repr(member.configuration)
        if form_key in self.forms:
            form = self.forms[form_key]
        else:
            form = Form(self.generate_id(), form_key)
            self.forms[form_key] = form
        form.incarnate()
        member.incarnated(form, form.reincarnations)
        member.prepare_epoch(self.epoch)
        member.prepare_round(self.round)
        self.members.append(member)
        return member

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        if not member.alive:
            raise RuntimeError("Member not alive")

        start_time = time.time()
        for component in self.controllers:
            component.evaluate_member(member)
            if not member.alive:
                break
        end_time = time.time()
        duration = end_time - start_time
        member.evaluated(duration)

    def contest_members(self, contestant1, contestant2):

        if not contestant1.alive and not contestant2.alive:
            raise RuntimeError("Contestants not alive")

        if contestant1.form is contestant2.form:
            raise RuntimeError("Contestants have duplicate forms")

        for component in self.controllers:
            component.contest_members(contestant1, contestant2)

    def judge_member(self, member):

        if not member.alive:
            raise RuntimeError("Member not alive")

        for component in self.controllers:
            component.judge_member(member)

    def bury_member(self, member):
        """
        Remove a member from the active pool
        """
        self.graveyard.append(member)
        self.members.remove(member)
        member.form.disembody()

    def rate_member(self, member):
        """
        Rate a member
        """

        if not member.alive:
            raise RuntimeError("Members is not alive")

        for component in self.controllers:
            component.rate_member(member)

    def rank_members(self):
        """
        Rank all members
        """
        inductees = [m for m in self.members if m.alive and m.league ]
        n_inductees = len(inductees)
        progress_prefix = "Rating %s" % self.name
        print("")
        if n_inductees > 0:
            for index in range(n_inductees):
                printProgressBar(index, n_inductees, prefix = progress_prefix, length = 50)
                self.rate_member(inductees[index])
            printProgressBar(n_inductees, n_inductees, prefix = progress_prefix, length = 50)

        candidates = [m for m in inductees if not m.rating is None]
        ranking = Ranking()
        if not candidates:
            ranking.inconclusive()
        else:
            candidates = sorted(candidates, key=lambda member: member.rating)
            ranking.conclusive(candidates)

        rank = len(candidates)
        for candidate in candidates:
            candidate.ranked(rank)
            rank -= 1
        self.ranking = ranking

    def start(self):
        """
        Perform simulation startup
        """
        self.epoch = 0
        self.round = 0
        self.step = 0
        self.hyper_parameters = [c for c in self.components if c.is_hyper_parameter() ]
        self.controllers = [c for c in self.components if c.is_controller() ]

        self.outline_simulation()
        for component in self.controllers:
            component.start_simulation(self)
        self.running = True

    def run_round(self):
        """
        Run a round of the simulation
        """
        self.round += 1
        random_state = self.random_state

        # Prepare for the next round
        members = self.list_members(alive = True)
        for member in members:
            member.prepare_round(self.round)

        # Judge all living members
        members = self.list_members(alive = True)
        for member in members:
            self.judge_member(member)

        # Repopulate
        members = self.list_members(alive = True)
        make_count = self.population_size - len(members)
        for make_index in range(make_count):
            self.make_member()

        # If we run out of search space the population can crash.
        # Make sure we don't get into an infinite loop.
        members = self.list_members(alive = True)
        if len(members) < 2:
            self.stop()
            return None

        # Ensure all members evaluated
        for member_index in range(len(members)):
            self.evaluate_member(members[member_index])
            printProgressBar(member_index + (self.round - 1) * self.population_size, self.rounds * self.population_size, prefix = "Evaluating %s epoch %s:" % (self.name, self.epoch), length = 50)

        # Contest members randomly
        members = self.list_members(alive = True)
        member_indexes = random_state.choice(len(members), size = len(members), replace = False)
        for member_index in range(0, len(members)-1, 2):
            self.contest_members(members[member_indexes[member_index]], members[member_indexes[member_index+1]])

        report_members = self.list_members()

        # Bury dead members
        dead_members = self.list_members(alive = False)
        for member in dead_members:
            self.bury_member(member)

        # Report on what happened
        for member in report_members:
            self.reports.append(self.record_member(member))

        printProgressBar(self.round * self.population_size, self.rounds * self.population_size, prefix = "Contesting %s epoch %s:" % (self.name, self.epoch), length = 50)

    def run_epoch(self, rounds):
        """
        Run an epoch
        """
        self.epoch += 1
        self.round = 0

        for component in self.controllers:
            component.start_epoch(self)

        members = self.list_members(alive = True)
        for member in members:
            member.prepare_epoch(self.epoch)

        for round in range(rounds):
            self.run_round()
            if not self.running:
                break

    def finish(self, reason):
        """
        Perform final simulation processing
        """
        self.running = False

        random_state = self.random_state
        members = self.members

        # Perform ranking
        self.rank_members()

        # Tell everyone we are done
        for member in members:
            member.finshed(reason)

        # final report on ranked members
        for member in self.ranking.members:
            self.reports.append(self.record_member(member))

    def stop(self):
        """
        Indicate that the simulation should stop
        """
        self.running = False

    def _simulation_finished(self, start_time, epochs, max_time):
        duration = time.time() - start_time
        return not self.running or self.epoch == epochs or (max_time is not None and duration >= max_time)

    def run(self, rounds, epochs, max_time = None):
        print("-----------------------------------------------------")
        start_time = time.time()
        today = datetime.datetime.now()

        self.epochs = epochs
        self.rounds = rounds
        print("Running %s - Started %s" % (self.name, today.strftime("%x %X")))
        self.start()

        finished = False
        while not finished:
            self.run_epoch(rounds)
            finished = self._simulation_finished(start_time, epochs, max_time)
            if finished:
                self.finish("finished")
            self.report()
        duration = time.time() - start_time
        print("%s finished - Duration %s" % (self.name, duration))

    def outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.properties.keys():
            outline.append_attribute(property_key, Dataset.Battle, [Role.Configuration])
        outline.append_attribute("epoch", Dataset.Battle, [Role.ID])
        outline.append_attribute("round", Dataset.Battle, [Role.ID])
        outline.append_attribute("step", Dataset.Battle, [Role.ID])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("form_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("incarnation", Dataset.Battle, [Role.Property])
        outline.append_attribute("event", Dataset.Battle, [Role.Property])
        outline.append_attribute("fault", Dataset.Battle, [Role.Property])

        outline.append_attribute("famous", Dataset.Battle, [Role.Property])
        outline.append_attribute("alive", Dataset.Battle, [Role.Property])
        outline.append_attribute("final", Dataset.Battle, [Role.Property])
        outline.append_attribute("ranking", Dataset.Battle, [ Role.KPI ])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        epoch = self.epoch
        round = self.round
        step = self.step

        record = Record()
        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])

        record.epoch = epoch
        record.round = round
        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation
        record.event_time = time.ctime(member.evaluation_time)
        record.event = member.event
        record.event_reason = member.event_reason

        record.rating = member.rating
        record.rating_sd = member.rating_sd
        record.ranking = member.ranking

        record.league = member.league
        record.alive = member.alive
        record.final = member.final

        for component in self.components:
            component.record_member(member, record)
        return record

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.controllers:
            component.report_simulation(self)
        self.reports = []
