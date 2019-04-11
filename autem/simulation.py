from .member import Member
from .epoch import Epoch
from .specie import Specie
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
    def __init__(self, name, components,
                seed = 1234, population_size = 10, round_size = 20, top_league = 4,
                max_reincarnations = 3, max_epochs = 10, max_time = None, n_jobs = -1, properties = {}):
        self.name = name
        self.components = components
        self.properties = properties
        self.population_size = population_size
        self.round_size = round_size
        self.top_league = top_league
        self.max_reincarnations = max_reincarnations
        self.n_jobs = n_jobs
        self.max_epochs = max_epochs
        self.max_time = max_time
        self.transmutation_rate = 0.5

        self.outline = None
        self.resources = SimpleNamespace()
        self.hyper_parameters = None
        self.controllers = None

        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1

        self.start_time = None
        self.end_time = None

        self.specie_id = None
        self.species = {}
        self.epoch_id = None
        self.epochs = {}
        self.members = []
        self.graveyard = []
        self.forms = {}
        self.reports = []

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def list_members(self, alive = None, top = None):
        """
        List members
        """

        def include_member(member):
            alive_passed = alive is None or member.alive == alive
            is_top = member.league == self.top_league
            top_passed = top is None or is_top == top
            return alive_passed and top_passed

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

    def make_member(self, reason):
        """
        Make a new member
        """

        specie = self.species[self.specie_id]

        # Find all makers
        makers = [ c for c in self.components if isinstance(c, Maker)]
        maker_indexes = self.random_state.choice(len(makers), size = len(makers), replace=False)

        # Invoke members in random order till one makes the member
        for maker_index in maker_indexes:
            member = makers[maker_index].make_member(specie)
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

        epoch = self.epochs[self.epoch_id]
        member.prepare_epoch(epoch.id)
        member.prepare_round(epoch.id, epoch.round)
        member.incarnated(epoch.id, form, form.reincarnations, reason)
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
        inductees = self.list_members(alive = True, top = True)
        n_inductees = len(inductees)
        progress_prefix = "Rating %s epoch %s:" % (self.name, self.epoch_id)
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
            candidate.ranked(self.epoch_id, rank)
            rank -= 1

        self.epochs[self.epoch_id].ranked(ranking)
        return ranking

    def run_round(self):
        """
        Run a round of the simulation
        """

        epoch = self.epochs[self.epoch_id]
        operation_name = "Evaluating %s epoch %s:" % (self.name, epoch.id)

        # Prepare for the next round
        epoch.prepare_round()
        members = self.list_members(alive = True)
        for member in members:
            member.prepare_round(epoch.id, epoch.round)

        # Promote all living members
        for member in members:
            if member.league < self.top_league:
                member.promote(epoch.id, "Fit")

        # Repopulate
        make_count = self.population_size - len(members)
        for make_index in range(make_count):
            self.make_member("Repopulate")

        # If we run out of search space the population can crash.
        # Make sure we don't get into an infinite loop.
        members = self.list_members(alive = True)
        if len(members) < 2:
            raise RuntimeError("Population crash")

        # Ensure all members evaluated
        for member_index in range(len(members)):
            self.evaluate_member(members[member_index])
            printProgressBar(member_index + (epoch.round - 1) * self.population_size, self.round_size * self.population_size, prefix = operation_name, length = 50)

        # Have all evaluation survivors contest each other
        members = self.list_members(alive = True)
        for member1_index in range(len(members)-1):
            for member2_index in range(member1_index+1, len(members)):
                self.contest_members(members[member1_index], members[member2_index])

        report_members = self.list_members()

        # Judge all members
        for member in self.list_members():
            self.judge_member(member)

        # Bury dead members
        for member in self.list_members(alive = False):
            self.bury_member(member)

        printProgressBar(epoch.round * self.population_size, self.round_size * self.population_size, prefix = operation_name, length = 50)

        # Report on what happened
        for member in report_members:
            self.reports.append(self.record_member(member))

    ## Epoch life-cycle

    def start_epoch(self):
        """
        Start a new epoch
        """
        specie = self.species[self.specie_id]
        self.epoch_id += 1
        epoch = Epoch(specie, self.epoch_id)
        self.epochs[self.epoch_id] = epoch

        epoch.prepare()
        for component in self.controllers:
            component.start_epoch(epoch)

        members = self.list_members(alive = True)
        for member in members:
            member.prepare_epoch(self.epoch_id)
        return epoch

    def finish_epoch(self):
        """
        Finish the current epoch
        """
        self.rank_members()

        epoch = self.epochs[self.epoch_id]
        for component in self.controllers:
            component.judge_epoch(epoch)
        epoch.finished()

    def should_finish_epoch(self):
        """
        Should we finish the epoch?
        """
        duration = time.time() - self.start_time
        epoch = self.epochs[self.epoch_id]

        if self.max_time is not None and duration >= self.max_time:
            return (True, "Max time")

        if epoch.round >= self.round_size:
            return (True, "Max rounds")
        
        return (False, None)

    def run_epoch(self):
        """
        Run an epoch
        """

        epoch = self.start_epoch()
        
        finished = False
        while not finished:
            self.run_round()
            finished, reason = self.should_finish_epoch()

        self.finish_epoch()

        finish_specie, reason = self.should_finish_specie()
        # If we should finish the species, finish and bury the members
        # before we report
        if finish_specie:
            for member in self.list_members(alive=True):
                member.finshed(epoch.id, reason)
                self.bury_member(member)

        # Final report for ranked members
        for member in epoch.ranking.members:
            self.reports.append(self.record_member(member))
        self.report()

        return epoch

    ## Species life-cycle

    def start_specie(self):
        """
        Start a new specie
        """
        specie_id = self.specie_id + 1
        specie = Specie(self, specie_id)
        self.specie_id = specie_id
        self.species[specie_id] = specie

        specie.prepare()
        for component in self.controllers:
            component.start_specie(specie)

        return specie

    def should_finish_specie(self):
        """
        Should we finish the species?
        """
        duration = time.time() - self.start_time
        epoch = self.epochs[self.epoch_id]

        if not epoch.progressed:
            return (True, "No progress")

        if epoch.id == self.max_epochs:
            return (True, "Max epochs")

        if self.max_time is not None and duration >= self.max_time:
            return (True, "Max time")
        
        return (False, None)

    def finish_specie(self):
        """
        Finish the current specie
        """
        specie = self.species[self.specie_id]
        for component in self.controllers:
            component.judge_specie(specie)
        specie.finished()

    def run_specie(self):
        """
        Run a a specie
        """

        specie = self.start_specie()

        finished = False
        while not finished:
            self.run_epoch()
            finished, reason = self.should_finish_specie()

        self.finish_specie()

        return specie

    ## Simulation life-cycle

    def start_simulation(self):
        """
        Perform simulation startup
        """
        self.start_time = time.time()
        self.specie_id = 0
        self.epoch_id = 0
        self.hyper_parameters = [c for c in self.components if c.is_hyper_parameter() ]
        self.controllers = [c for c in self.components if c.is_controller() ]
        self.outline_simulation()
        for component in self.controllers:
            component.start_simulation(self)

    def should_finish_simulation(self):
        """
        Should we finish the simulation?
        """
        duration = time.time() - self.start_time
        epoch = self.epochs[self.epoch_id]

        if not epoch.progressed:
            return (True, "No progress")

        if epoch.id == self.max_epochs:
            return (True, "Max epochs")

        if self.max_time is not None and duration >= self.max_time:
            return (True, "Max time")
        
        return (False, None)

    def finish_simulation(self):
        """
        Perform simulation finish
        """
        self.end_time = time.time()

    def run(self):

        print("-----------------------------------------------------")
        today = datetime.datetime.now()
        print("Running %s - Started %s" % (self.name, today.strftime("%x %X")))

        self.start_simulation()

        finished = False
        while not finished:
            self.run_specie()
            finished, reason = self.should_finish_simulation()

        self.finish_simulation()
        duration = self.end_time - self.start_time
        print("%s - %s - Duration %s" % (self.name, reason, duration))

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

        outline.append_attribute("ranking", Dataset.Battle, [ Role.KPI ])
        outline.append_attribute("incarnation_epoch", Dataset.Battle, [ Role.Property ])

        outline.append_attribute("league", Dataset.Battle, [Role.Property])
        outline.append_attribute("final", Dataset.Battle, [Role.Property])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        epoch_id = self.epoch_id
        epoch = self.epochs[epoch_id]
        round = epoch.round
        step = (epoch_id - 1) * self.round_size + round

        record = Record()
        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])

        record.epoch = epoch_id
        record.round = round
        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation
        record.incarnation_epoch = member.incarnation_epoch_id
        record.event_time = time.ctime(member.evaluation_time)
        record.event = member.event
        record.event_reason = member.event_reason

        record.rating = member.rating
        record.rating_sd = member.rating_sd
        record.ranking = member.ranking

        record.league = member.league
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
