from .member import Member
from .outcome import OutcomeType, Outcome
from .evaluation import Evaluation
from .record import Record
from .dataset import Dataset
from .role import Role
from .outline import Outline
from .form import Form

from types import SimpleNamespace

import numpy

class Simulation:

    """Simulation state"""
    def __init__(self, name, components, seed = 1234, population_size = 10):
        self.name = name
        self.components = components
        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1
        self.population_size = population_size
        self.outline = None
        self.resources = SimpleNamespace()
        self.members = []
        self.forms = {}
        self.reincarnations = []
        self.reports = []
        self.contests = []
        self.n_steps = 0
        self.running = False
        self.stopping = False

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def make_member(self):
        """
        Create a brand new member
        """
        member = Member(self)
        for component in self.components:
            component.start_member(member)
        return member

    def incarnate_member(self, member):
        """
        Given a member that is not currently incarnated, incarnate it
        """
        if not member.form is None:
            raise RuntimeError("Member has already been incarnated")
        form = Form(member)
        form_key = form.get_key()
        if form_key in self.forms:
            form = self.forms[form_key]
        else:
            self.forms[form_key] = form
        form.count += 1
        member.incarnating()
        member.incarnated(form)
        self.members.append(member)

    def start_member(self):
        """
        Start a new member
        """
        member = self.make_member()
        self.incarnate_member(member)
        return member

    def make_member_copy(self, prior):
        """
        Create a member thats configured as a copy of another
        """
        member = Member(self)
        for component in self.components:
            component.copy_member(member, prior)
        return member

    def make_member_crossover(self, parent1, parent2):
        """
        Create a member that is a cross over of two parents
        """
        member = Member(self)
        for component in self.components:
            component.crossover_member(member, parent1, parent2)
        return member

    def mutate_member(self, member):
        """
        Mutate a member, making a guaranteed modification to its configuration
        """
        random_state = self.random_state
        components = self.components
        n_components = len(components)
        # Try each component in a random order until a component claims to have mutated the state
        prior_repr = repr(member.configuration)
        component_indexes = random_state.choice(n_components, size=n_components, replace=False)
        for component_index in component_indexes:
            component = components[component_index]
            mutated = component.mutate_member(member)
            if mutated:
                if repr(member.configuration) == prior_repr:
                    raise RuntimeError("Configuration was not mutated as requested")
                return True
        return False

    def crossover_member(self, parent1, parent2, max_incarnations = 5):
        """
        Cross over 2 members
        """
        member = self.make_member_crossover(parent1, parent2)
        self.incarnate_member(member)
        return member

    def reincarnate_member(self, prior):
        """
        Reincarnate a prior member. 
        Reincarnate reintroduces a member with variations in configuration
        """
        member = self.make_member_copy(prior)

        # Config should be the same
        if repr(member.configuration) != repr(prior.configuration):
            raise RuntimeError("Form was not duplicated")

        # Perform mutations until we have a new form
        find_attempts = 0
        max_attempts = 100
        random_state = self.random_state
        reincarnated = False
        while not reincarnated:
            member.incarnating()
            mutated = self.mutate_member(member)
            if not mutated:
                break
            if member.birth > max_attempts:
                break
            form_key = repr(member.configuration)
            reincarnated = not form_key in self.forms

        if reincarnated:
            # Complete the reincarnation
            self.incarnate_member(member)
            self.reincarnations.remove(prior)
        else:
            # Reincarnation failed!
            self.reincarnations.remove(prior)
            member.killed()
        return member

    def _outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("step", Dataset.Battle, [Role.Dimension])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("birth", Dataset.Battle, [Role.Property])
        outline.append_attribute("death", Dataset.Battle, [Role.Property])
        outline.append_attribute("incarnation", Dataset.Battle, [Role.Property])
        outline.append_attribute("n_evaluation", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_errors", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_contest", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_victory", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_defeat", Dataset.Battle, [Role.Measure])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def start(self):
        """
        Perform simulation startup
        """
        self._outline_simulation()
        for component in self.components:
            component.start_simulation(self)
        for index in range(self.population_size):
            self.start_member()
        for member in self.members:
            self.reports.append(self.record_member(member))

        if len(self.members) < 2:
            raise RuntimeError("Require at least 2 members to start")
        self.running = True

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        member_id = member.id
        evaluation = Evaluation(member_id)
        for component in self.components:
            try:
                component.evaluate_member(member, evaluation)
            except Exception as ex:
                evaluation.failed(ex)
                break

        member.evaluations.append(evaluation)
        return evaluation

    def contest_members(self, contestant1, contestant2):
        contest = Outcome(self.n_steps, contestant1.id, contestant2.id)
        contestant1.grown()
        contestant2.grown()

        if contestant1.form is contestant2.form:
            # If the contestants have the same form mark that they are duplicated
            contest.duplicated()
            return contest

        for component in self.components:
            component.contest_members(contestant1, contestant2, contest)
        contestant1.contested(contest)
        contestant2.contested(contest)
        self.contests.append(contest)
        return contest

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        step = self.n_steps
        record = Record()
        record.step = step
        record.member_id = member_id
        record.birth = member.birth
        record.death = member.dead

        record.incarnation = member.incarnation
        record.n_evaluation = len(member.evaluations)
        record.n_errors = sum(e.errors for e in member.evaluations)
        record.n_contest = len(member.contests)
        record.n_victory = member.n_victory
        record.n_defeat = member.n_defeat

        if record.n_errors == 0:
            for component in self.components:
                component.record_member(member, record)
        return record

    def should_repopulate(self):
        """
        Should we try to repopulate?
        """
        return self.running and not self.stopping and self.population_size > len(self.members)

    def step(self):
        """
        Run a step of the simulation
        """

        if not self.running:
            raise RuntimeError("Simulation is not running")

        random_state = self.random_state
        members = self.members

        # Pick 2 members
        contestant_indexes = random_state.choice(len(members), 2, replace=False)
        contestant1 = members[contestant_indexes[0]]
        contestant2 = members[contestant_indexes[1]]

        # Tell them they are grown
        contest = self.contest_members(contestant1, contestant2)

        # Have them contest.

        # If there was no contest then something is wrong
        if contest.is_uncontested():
            raise RuntimeError("No contest component defined")

        # If we can't tell anything we need to do more evaluation
        if contest.is_inconclusive():
            evaluation1 = self.evaluate_member(contestant1)
            evaluation2 = self.evaluate_member(contestant2)

            # Kill contestants immediately for an error was generated during evaluation
            # They are no use to us
            if evaluation1.errors > 0:
                contestant1.killed()
                self.members.remove(contestant1)

            if evaluation2.errors > 0:
                contestant2.killed()
                self.members.remove(contestant2)

        # If contest was fatal remove the loser
        if contest.is_fatal():
            loser = contestant1 if contest.loser_id() == contestant1.id else contestant2
            loser.killed()
            self.members.remove(loser)

        # If contest was duplication then move the later incarnation into the reincarnation queue
        if contest.is_duplicated():
            duplicate = contestant1 if contestant1.incarnation > contestant2.incarnation else contestant2
            duplicate.killed()
            self.members.remove(duplicate)
            self.reincarnations.append(duplicate)

        # Repopulate!
        newborn = None
        if self.should_repopulate():
            if self.reincarnations:
                prior = self.reincarnations[0]
                newborn = self.reincarnate_member(prior)

        # Report on what happened
        self.n_steps += 1
        self.reports.append(self.record_member(contestant1))
        self.reports.append(self.record_member(contestant2))
        if not newborn is None:
            self.reports.append(self.record_member(newborn))

        if len(self.members) < 2:
            self.running = False

    def stop(self):
        """
        Indicate that the simulation should start stopping
        """
        self.stopping = True

    def run(self, steps):
        """
        Run the simulation for a number of steps
        """
        for step in range(steps):
            if not self.running:
                break
            self.step()

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.components:
            component.report_simulation(self)
        self.reports = []
    