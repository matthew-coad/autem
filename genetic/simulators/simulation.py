from .member import Member
from .outcome import OutcomeType, Outcome
from .evaluation import Evaluation
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

    def mature_member(self, member):
        member.matured()

    def honour_member(self, member):
        member.honour()

    def chastise_member(self, member):
        member.chastise()

    def hubbify_member(self, member):
        member.hubbify()

    def kill_member(self, member, cause_death, fault):
        member.killed(cause_death, fault)
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

        outline.append_attribute("mature", Dataset.Battle, [Role.Property])
        outline.append_attribute("attractive", Dataset.Battle, [Role.Property])
        outline.append_attribute("evaluations", Dataset.Battle, [Role.Property])
        outline.append_attribute("victories", Dataset.Battle, [Role.Property])
        outline.append_attribute("defeats", Dataset.Battle, [Role.Property])

        outline.append_attribute("n_alive", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_mature", Dataset.Battle, [Role.Measure])
        outline.append_attribute("n_attractive", Dataset.Battle, [Role.Measure])

        # Rankings
        outline.append_attribute("step", Dataset.Ranking, [Role.ID])
        outline.append_attribute("member_id", Dataset.Ranking, [Role.ID])

        outline.append_attribute("incarnation", Dataset.Ranking, [Role.Property])
        outline.append_attribute("rank", Dataset.Ranking, [Role.Property])

        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

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

        member.evaluated(evaluation)
        return evaluation

    def contest_members(self, contestant1, contestant2):
        contest = Outcome(self.n_steps, contestant1.id, contestant2.id)

        if contestant1.form is contestant2.form:
            # If the contestants have the same form mark that they are duplicated
            contest.duplicated()
            return contest

        for component in self.components:
            component.contest_members(contestant1, contestant2, contest)
        contestant1.contested(contest)
        contestant2.contested(contest)
        return contest

    def rank_members(self):
        """
        Rank all members
        """
        ranking = Ranking(self.n_steps)
        for component in self.components:
            component.rank_members(self, ranking)
        if ranking.is_equivalent(self.ranking):
            ranking.static(self.ranking)
        self.ranking = ranking
        return self.ranking

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

        record.mature = member.mature
        record.attractive = member.attractive
        record.evaluations = member.evaluations
        record.victories = member.victories
        record.defeats = member.defeats

        record.n_alive = member.n_alive
        record.n_mature = member.n_mature
        record.n_attractive = member.n_attractive

        for component in self.components:
            component.record_member(member, record)
        return record

    def record_ranking(self, member, rank):
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
        record.rank = rank
        for component in self.components:
            component.record_ranking(member, record)
        return record

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

        # If we can't tell anything we need to do more evaluation
        if contest.is_inconclusive():
            evaluation1 = self.evaluate_member(contestant1)
            evaluation2 = self.evaluate_member(contestant2)

            # Kill contestants immediately for an error was generated during evaluation
            # They are no use to us
            if evaluation1.errors > 0:
                self.kill_member(contestant1, "fault", evaluation1.fault)

            if evaluation2.errors > 0:
                self.kill_member(contestant2, "fault", evaluation2.fault)

        # If the contest was conclusive then the members are now mature
        if contest.is_conclusive():
            self.mature_member(contestant1)
            self.mature_member(contestant2)

        # If the contest was conclusive then hand out the laurels
        if contest.is_conclusive():
            winner = contestant1 if contest.victor_id() == contestant1.id else contestant2
            self.honour_member(winner)
            loser = contestant1 if contest.loser_id() == contestant1.id else contestant2
            self.chastise_member(loser)

        # If contest was fatal remove the loser
        if contest.is_fatal():
            self.kill_member(loser, "fatality", None)

        # If contest was classy mark the winner as attrative
        if contest.is_classy():
            self.hubbify_member(winner)

        # If contest was between members with duplicate forms kill the later incarnation
        if contest.is_duplicated():
            duplicate = contestant1 if contestant1.incarnation > contestant2.incarnation else contestant2
            self.kill_member(duplicate, "duplicate", None)

        # Repopulate!
        newborn = None
        if self.should_repopulate():
            candidates = [ m for m in self.members if m.alive and m.mature ]
            if len(candidates) >= 2:
                parent_indexes = random_state.choice(len(candidates), 2, replace=False)
                parent1 = candidates[parent_indexes[0]]
                parent2 = candidates[parent_indexes[1]]
                newborn = self.crossover_member(parent1, parent2)

        # Report on what happened
        self.n_steps += 1
        self.contest_reports.append(self.record_member(contestant1))
        self.contest_reports.append(self.record_member(contestant2))
        if not newborn is None:
            self.contest_reports.append(self.record_member(newborn))

        # Perform ranking
        ranking = self.rank_members()
        if ranking.is_conclusive() and ranking.original_step == self.n_steps:
            top_rank = ranking.members[0]
            self.ranking_reports.append(self.record_ranking(top_rank, 1))

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

        if not self.ranking_reports and self.ranking.is_conclusive():
            top_rank = self.ranking.members[0]
            self.ranking_reports.append(self.record_ranking(top_rank, 1))

        for component in self.components:
            component.report_simulation(self)
        self.contest_reports = []
        self.ranking_reports = []
    