from .member import Member
from .outcome import OutcomeType, Outcome
from .record import Record
from .dataset import Dataset
from .role import Role
from .outline import Outline
from .form import Form
from .ranking import Ranking

from types import SimpleNamespace

import numpy

class Simulation:

    """Simulation state"""
    def __init__(self, name, components, seed = 1234, population_size = 10, properties = {}):
        self.name = name
        self.components = components
        self.properties = properties
        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1
        self.population_size = population_size
        self.outline = None
        self.resources = SimpleNamespace()
        self.members = []
        self.forms = {}
        self.ranking = None
        self.contest_reports = []
        self.ranking_reports = []
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
        Incarnate the selected member
        """
        if not member.form is None:
            raise RuntimeError("Member has already been incarnated")
        form_key = repr(member.configuration)
        if form_key in self.forms:
            form = self.forms[form_key]
        else:
            form = Form(self.generate_id(), form_key)
            self.forms[form_key] = form
        form.count += 1
        member.incarnated(form, form.count)
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
        attempts = 0
        max_attempts = 100
        searching = True
        while searching:
            attempts += 1
            if attempts > max_attempts:
                # If after 100 tries we can't find a new form return nothing
                return None
            form_key = repr(member.configuration)
            if form_key in self.forms:
                self.mutate_member(member)
            else:
                searching = False
        self.incarnate_member(member)
        return member

    def hubbify_member(self, member):
        member.hubbify()

    def kill_member(self, member, cause_death):
        member.killed(cause_death)
        self.members.remove(member)

    def outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.properties.keys():
            outline.append_attribute(property_key, Dataset.Battle, [Role.Configuration])
        outline.append_attribute("step", Dataset.Battle, [Role.ID])
        outline.append_attribute("member_id", Dataset.Battle, [Role.ID])
        outline.append_attribute("form_id", Dataset.Battle, [Role.ID])

        outline.append_attribute("incarnation", Dataset.Battle, [Role.Property])
        outline.append_attribute("alive", Dataset.Battle, [Role.Property])
        outline.append_attribute("cause_death", Dataset.Battle, [Role.Property])
        outline.append_attribute("fault", Dataset.Battle, [Role.Property])

        outline.append_attribute("contests", Dataset.Battle, [Role.Property])
        outline.append_attribute("standoffs", Dataset.Battle, [Role.Property])
        outline.append_attribute("victories", Dataset.Battle, [Role.Property])
        outline.append_attribute("defeats", Dataset.Battle, [Role.Property])

        outline.append_attribute("accuracy", Dataset.Battle, [ Role.Measure ])
        outline.append_attribute("maturity", Dataset.Battle, [Role.Measure])
        outline.append_attribute("mature", Dataset.Battle, [Role.Property])
        outline.append_attribute("robustness", Dataset.Battle, [Role.Property])
        outline.append_attribute("fatality", Dataset.Battle, [Role.Property])
        outline.append_attribute("attractiveness", Dataset.Battle, [Role.Property])
        outline.append_attribute("attractive", Dataset.Battle, [Role.Property])

        outline.append_attribute("rating", Dataset.Battle, [ Role.KPI ])
        outline.append_attribute("ranking", Dataset.Battle, [ Role.KPI ])

        # Rankings
        outline.append_attribute("step", Dataset.Ranking, [Role.ID])
        outline.append_attribute("member_id", Dataset.Ranking, [Role.ID])

        outline.append_attribute("incarnation", Dataset.Ranking, [Role.Property])
        outline.append_attribute("ranking", Dataset.Ranking, [Role.Property])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def prepare_member(self, member):
        """
        Perform once off member preparation
        """
        if member.ready:
            raise RuntimeError("Member already prepared")

        if member.fault is None:
            for component in self.components:
                try:
                    component.prepare_member(member)
                except Exception as ex:
                    member.failed(ex)
                    break
            member.prepared()

        # Kill contestants immediately for an error was generated
        # They are of no use to us
        if not member.fault is None:
            self.kill_member(member, "prepare fault")

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        if not member.ready:
            self.prepare_member(member)

        if member.alive:
            for component in self.components:
                try:
                    component.evaluate_member(member)
                except Exception as ex:
                    member.failed(ex)
                    break

        # Kill contestants immediately for an error was generated during evaluation
        # They are of no use to us
        if member.alive and not member.fault is None:
            self.kill_member(member, "evaluate fault")

    def contest_members(self, contestant1, contestant2):
        outcome = Outcome(self.n_steps, contestant1.id, contestant2.id)

        if contestant1.form is contestant2.form:
            # If the contestants have the same form mark that they are duplicated
            outcome.duplicated()
            duplicate = contestant1 if contestant1.incarnation > contestant2.incarnation else contestant2
            self.kill_member(duplicate, "duplicate")
            return outcome

        for component in self.components:
            component.contest_members(contestant1, contestant2, outcome)

        if outcome.is_inconclusive():
            contestant1.stand_off()
            contestant2.stand_off()

        if outcome.is_conclusive():
            winner = contestant1 if outcome.victor_id() == contestant1.id else contestant2
            winner.honour()
            loser = contestant1 if outcome.loser_id() == contestant1.id else contestant2
            loser.chastise()

        return outcome

    def stress_members(self, contestant1, contestant2, outcome):
        for component in self.components:
            component.stress_members(contestant1, contestant2, outcome)

        if contestant1.fatality == 1:
            self.kill_member(contestant1, "fatality")

        if contestant2.fatality == 1:
            self.kill_member(contestant2, "fatality")

    def rate_member(self, member):
        """
        Rate a member
        """

        if not member.alive or not member.mature or not member.attractive:
            return None

        for component in self.components:
            try:
                component.rate_member(member)
            except Exception as ex:
                member.failed(ex)
                break

        # Kill contestants immediately for an error was generated during evaluation
        # They are of no use to us
        if member.alive and not member.fault is None:
            self.kill_member(member, "rate fault")

    def rank_members(self):
        """
        Rank all members
        """

        # Generate ratings if needed
        for member in self.members[:]:
            self.rate_member(member)

        ranking = Ranking(self.n_steps)
        candidates = [m for m in self.members if not m.rating is None]
        if not candidates:
            ranking.inconclusive()
        else:
            candidates = sorted(candidates, key=lambda member: member.rating)
            ranking.conclusive(candidates)

        if ranking.is_equivalent(self.ranking):
            ranking.static(self.ranking)
        else:
            for rank in range(len(ranking.members)):
                ranking.members[rank].rank(rank + 1)
        self.ranking = ranking

    def should_repopulate(self):
        """
        Should we try to repopulate?
        """
        return self.running and not self.stopping and self.population_size > len(self.members)

    def start(self):
        """
        Perform simulation startup
        """
        self.outline_simulation()
        for component in self.components:
            component.start_simulation(self)
        for index in range(self.population_size):
            self.start_member()
        for member in self.members:
            self.contest_reports.append(self.record_member(member))
        if len(self.members) < 2:
            raise RuntimeError("Require at least 2 members to start")
        self.running = True

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

        # If the contest was conclusive then determine the contestants fate!
        if contest.is_conclusive():
            self.stress_members(contestant1, contestant2, contest)

        # If we can't tell anything we need to do more evaluation
        if contest.is_inconclusive():
            self.evaluate_member(contestant1)
            self.evaluate_member(contestant2)

        # Repopulate!
        newborn = None
        if self.should_repopulate():
            candidates = [ m for m in self.members if m.alive and m.mature ]
            if len(candidates) >= 2:
                parent_indexes = random_state.choice(len(candidates), 2, replace=False)
                parent1 = candidates[parent_indexes[0]]
                parent2 = candidates[parent_indexes[1]]
                newborn = self.crossover_member(parent1, parent2)

        # Perform ranking
        self.rank_members()

        # Report on what happened
        self.n_steps += 1
        self.contest_reports.append(self.record_member(contestant1))
        self.contest_reports.append(self.record_member(contestant2))
        if not newborn is None:
            self.contest_reports.append(self.record_member(newborn))

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

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        step = self.n_steps
        record = Record()

        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])

        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation
        record.alive = member.alive
        record.cause_death = member.cause_death
        record.fault = str(member.fault)

        record.contests = member.contests
        record.standoffs = member.standoffs
        record.victories = member.victories
        record.defeats = member.defeats

        record.accuracy = member.accuracy
        record.maturity = member.maturity
        record.mature = member.mature
        record.robustness = member.robustness
        record.fatality = member.fatality
        record.attractiveness = member.attractiveness
        record.attractive = member.attractive

        record.rating = member.rating
        record.ranking = member.ranking

        if member.fault is None:
            for component in self.components:
                component.record_member(member, record)
        return record

    def record_ranking(self, member):
        """
        Generate a record on a member ranking
        """
        member_id = member.id
        record = Record()
        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])
        step = self.n_steps
        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation

        record.rating = member.rating
        record.ranking = member.ranking

        if member.fault is None:
            for component in self.components:
                component.record_ranking(member, record)
        return record

    def report(self):
        """
        Report on progress of the simulation
        """

        #if not self.ranking_reports and self.ranking.is_conclusive():
        #    top_rank = self.ranking.members[0]
        #    self.ranking_reports.append(self.record_ranking(top_rank, 1))

        for component in self.components:
            component.report_simulation(self)
        self.contest_reports = []
        self.ranking_reports = []
    