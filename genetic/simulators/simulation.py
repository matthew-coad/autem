from .member import Member
from .battle_result import BattleOutcome, BattleResult
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

    def battle_members(self, contestant1, contestant2):
        result = BattleResult(contestant1.id, contestant2.id)
        for component in self.components:
            component.battle_members(contestant1, contestant2, result)
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
        result = self.battle_members(contestant1, contestant2)

        # Inconclusive. Not enough information to evaluate
        if result.outcome == BattleOutcome.NoContest:
            raise RuntimeError("No battle component provided")
        elif result.outcome == BattleOutcome.Inconclusive:
            self.evaluate_member(contestant1)
            self.evaluate_member(contestant2)
        elif result.outcome == BattleOutcome.Indecisive:
            report = True
            contestant1.matched(result)
            contestant2.matched(result)
        elif result.outcome == BattleOutcome.Decisive:
            report = True
            contestant1.matched(result)
            contestant2.matched(result)
        else:
            raise RuntimeError("Unexpected outcome")

        # Perform tracking
        self.n_steps += 1
        report = result.outcome == BattleOutcome.Inconclusive or result.outcome == BattleOutcome.Decisive
        if report:
            self.reports.append(self.record_member(contestant1))
            self.reports.append(self.record_member(contestant2))
        
        # Member 1 Decisive Victory
        # Member 1 Indecisive Victory
        # Member 2 Decisive Victory
        # Member 2 Indecisive Victory

        # If inconclusive run evaluation for both members

        # If a victor allocate hitpoints. Looser, loose. Victor gain.

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
    