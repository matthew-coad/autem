from .member import Member
from .outcome import OutcomeType, Outcome
from .evaluation import Evaluation
from .record import Record
from .outline import Outline, Dataset, Role

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
        self.reports = []
        self.n_steps = 0

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def start_member(self, member):
        """
        Start a simulation member
        """
        for component in self.components:
            component.start_member(member)

    def _outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("step", Dataset.Battle, [Role.Dimension])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("n_evaluation", Dataset.Battle, [Role.Measure])
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
            member = Member(self)
            self.members.append(member)
            self.start_member(member)

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
        result = Outcome(contestant1.id, contestant2.id)
        for component in self.components:
            component.contest_members(contestant1, contestant2, result)
        return result

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        step = self.n_steps
        record = Record()
        record.step = step
        record.member_id = member_id
        record.n_evaluation = len(member.evaluations)
        record.n_contest = len(member.contests)
        record.n_victory = member.n_victory
        record.n_defeat = member.n_defeat

        for component in self.components:
            component.record_member(member, record)
        return record

    def step(self):
        """
        Run a step of the simulation
        """

        random_state = self.random_state
        members = self.members

        # Pick 2 members
        contestant_indexes = random_state.choice(len(members), 2, replace=False)
        contestant1 = members[contestant_indexes[0]]
        contestant2 = members[contestant_indexes[1]]

        # Have them battle.
        outcome = self.contest_members(contestant1, contestant2)
        contestant1.contested(outcome)
        contestant2.contested(outcome)

        # If there was no contest then something is wrong
        if outcome.is_uncontested():
            raise RuntimeError("No contest component defined")

        # If we can't tell anything we need to do more evaluation
        if outcome.is_inconclusive():
            self.evaluate_member(contestant1)
            self.evaluate_member(contestant2)

        # Report on what happened
        self.n_steps += 1
        self.reports.append(self.record_member(contestant1))
        self.reports.append(self.record_member(contestant2))
        
        # Member 1 Decisive Victory
        # Member 1 Indecisive Victory
        # Member 2 Decisive Victory
        # Member 2 Indecisive Victory

        # For each member compare their win loss ratio against the history of other members
        # If its significant consider killing/breeding

        # If victory is indecisive consider breeding members 

    def report(self):
        """
        Report on progress of the simulation
        """
        for component in self.components:
            component.report_simulation(self)
        self.reports = []
    