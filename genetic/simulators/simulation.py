from .member import Member
from .outcome import OutcomeType, Outcome
from .evaluation import Evaluation
from .record import Record
from .outline import Outline, Dataset, Role
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
        self.reports = []
        self.contests = []
        self.n_steps = 0
        self.running = False

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def start_member(self):
        member = Member(self)
        for component in self.components:
            component.start_member(member)
        form = Form(member)
        form_key = form.get_key()
        if form_key in self.forms:
            form = self.forms[form_key]
        else:
            self.forms[form_key] = form
        form.count += 1
        self.members.append(member)
        member.incarnated(form)

    def _outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("step", Dataset.Battle, [Role.Dimension])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("incarnation", Dataset.Battle, [Role.Property])
        outline.append_attribute("n_evaluation", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_contest", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_victory", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_defeat", Dataset.Battle, [Role.Measure])
        outline.append_attribute("dead", Dataset.Battle, [Role.Property])

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
            component.evaluate_member(member, evaluation)
        member.evaluations.append(evaluation)
        return evaluation

    def contest_members(self, contestant1, contestant2):
        contest = Outcome(self.n_steps, contestant1.id, contestant2.id)
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
        record.incarnation = member.incarnation
        record.n_evaluation = len(member.evaluations)
        record.n_contest = len(member.contests)
        record.n_victory = member.n_victory
        record.n_defeat = member.n_defeat
        record.dead = member.dead

        for component in self.components:
            component.record_member(member, record)
        return record

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

        # Have them contest.
        contest = self.contest_members(contestant1, contestant2)

        # If there was no contest then something is wrong
        if contest.is_uncontested():
            raise RuntimeError("No contest component defined")

        # If we can't tell anything we need to do more evaluation
        if contest.is_inconclusive():
            self.evaluate_member(contestant1)
            self.evaluate_member(contestant2)

        # Report on what happened
        self.n_steps += 1
        self.reports.append(self.record_member(contestant1))
        self.reports.append(self.record_member(contestant2))

        # If contest was fatal remove the loser
        if contest.is_fatal():
            loser = contestant1 if contest.loser_id() == contestant1.id else contestant2
            self.members.remove(loser)

        if len(self.members) < 2:
            self.running = False

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
    