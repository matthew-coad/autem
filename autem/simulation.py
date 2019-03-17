from .member import Member
from .outcome import OutcomeType, Outcome
from .record import Record
from .dataset import Dataset
from .role import Role
from .outline import Outline
from .form import Form
from .ranking import Ranking
from types import SimpleNamespace
from .feedback import printProgressBar
from .choice import Choice

import numpy
import time

class Simulation:

    """Simulation state"""
    def __init__(self, name, components, seed = 1234, population_size = 10, top_league = 6, properties = {}, n_jobs = -1):
        self.name = name
        self.components = components
        self.properties = properties
        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1
        self.population_size = population_size
        self.top_league = 6
        self.outline = None
        self.resources = SimpleNamespace()
        self.hyper_parameters = None
        self.controllers = None
        self.initial_mutations = []
        self.members = []
        self.graveyard = []
        self.failures = []
        self.forms = {}
        self.ranking = None
        self.reports = []
        self.n_steps = 0
        self.epoch = None
        self.running = False
        self.n_jobs = n_jobs
        self.transmutation_rate = 0.5

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

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

    def mutate_member(self, member, transmute):
        """
        Mutate a member, making a guaranteed modification to its configuration
        """
        prior_repr = repr(member.configuration)
        random_state = self.random_state
        components = self.hyper_parameters
        n_components = len(components)
        initial_mutations = self.initial_mutations

        if initial_mutations:
            mutation_index = random_state.randint(0, len(initial_mutations))
            mutation = initial_mutations[mutation_index]
            del initial_mutations[mutation_index]
            group_name = mutation["group_name"]
            choice_name = mutation["choice_name"]
            choice = [ c for c in components if c.name == group_name ][0]
            choice.force_member(member, choice_name)
            return True

        # Work out the component probabilities based on their importance
        # total_p = sum((c.importance for c in components))
        # component_p = [c.importance / total_p for c in components]

        # Try each component in a random order until a component claims to have mutated the state
        # component_indexes = random_state.choice(n_components, size=n_components, replace=False, p=component_p)
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
        searching = True
        random_state = self.random_state
        # Sometimes transmute the first mutation attept
        transmute = random_state.random_sample() <= self.transmutation_rate
        while searching:
            attempts += 1
            if attempts > max_attempts:
                # If after 100 tries indicate that we failed
                return False
            form_key = repr(member.configuration)
            if form_key in self.forms:
                self.mutate_member(member, transmute)
                transmute = False
            else:
                searching = False
        return True

    def make_initial_mutations(self):
        """
        Make initial member muations list
        The initial mutation list ensures that every component choice gets selected a minimum number of times
        """
        mutations = []
        for repeat in range(2):
            for component in self.hyper_parameters:
                if isinstance(component, Choice):
                    choice_names = component.get_component_names()
                    for choice_name in choice_names:
                        mutations.append( { "repeat": repeat, "group_name": component.name, "choice_name": choice_name } )
        self.initial_mutations = mutations

    def make_member(self):
        """
        Make a new member
        """
        member = Member(self)
        for component in self.hyper_parameters:
            component.initialize_member(member)
        specialized = self.specialize_member(member)
        if specialized:
            self.incarnate_member(member)
            return member
        else:
            return None

    def crossover_member(self, parent1, parent2):
        """
        Cross over 2 members
        """
        member = Member(self)
        for component in self.hyper_parameters:
            component.crossover_member(member, parent1, parent2)
        specialized = self.specialize_member(member)
        if specialized:
            self.incarnate_member(member)
            return member
        else:
            return None

    def prepare_member(self, member):
        """
        Perform once off member preparation
        """
        if not member.alive:
            raise RuntimeError("Member is not alive")

        if member.starts:
            raise RuntimeError("Member already started")

        for component in self.hyper_parameters:
            component.prepare_member(member)
            if not member.alive:
                break

        if member.alive:
            member.started()

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        if not member.started:
            raise RuntimeError("Member not started")

        if not member.alive:
            raise RuntimeError("Member not alive")

        for component in self.controllers:
            component.evaluate_member(member)
            if not member.alive:
                break
        if member.alive:
            member.evaluated()

    def contest_members(self, contestant1, contestant2):

        if not contestant1.alive and not contestant2.alive:
            raise RuntimeError("Contestants not alive")

        if contestant1.form is contestant2.form:
            raise RuntimeError("Contestants have duplicate forms")

        outcome = Outcome(self.n_steps, contestant1.id, contestant2.id)
        for component in self.controllers:
            component.contest_members(contestant1, contestant2, outcome)

        if contestant1.alive and contestant2.alive:

            if outcome.is_inconclusive():
                contestant1.stand_off()
                contestant2.stand_off()

            if outcome.is_zero_sum():
                winner = contestant1 if outcome.victor_id() == contestant1.id else contestant2
                winner.victory()
                loser = contestant1 if outcome.loser_id() == contestant1.id else contestant2
                loser.defeat()
        return outcome

    def judge_members(self, contestant1, contestant2, outcome):

        if not contestant1.alive or not contestant2.alive:
            raise RuntimeError("Contestants not alive")

        for component in self.controllers:
            component.judge_members(contestant1, contestant2, outcome)

    def bury_member(self, member):
        """
        Remove a member from the active pool and move them to the graveyard
        """
        self.members.remove(member)
        self.graveyard.append(member)

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
        ranking = Ranking(self.n_steps)
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

    def choose_competitors(self):
        # Choose one contestant at random
        candidates = self.members
        if len(candidates) < 2:
            raise RuntimeError("Need at least 2 members to choose from")
        random_state = self.random_state
        contestant1_index = random_state.choice(len(candidates))
        contestant1 = candidates[contestant1_index]

        #maximum_league = max(c.league for c in candidates)
        #minimum_league = contestant1.league
        #candidates2 = []
        #while not candidates2:
        #    if minimum_league < 0:
        #        raise RuntimeError("Could not find competitor as expected")
        #    candidates2 = [ c for c in candidates if c.id != contestant1.id and c.league >= minimum_league ]
        #    minimum_league -= 1
        # contestant2_weights = [ c.league + 1 for c in candidates2]
        candidates2 = [ c for c in candidates if c.id != contestant1.id ]
        contestant2_weights = [ 1 for c in candidates2]
        contestant2_p = [ w / sum(contestant2_weights) for w in contestant2_weights]
        contestant2_index = random_state.choice(len(candidates2), p = contestant2_p)
        contestant2 = candidates2[contestant2_index]
        return (contestant1, contestant2)

    def repopulate(self, parent1, parent2):
        current_population = len(self.members)
        repopulate = self.running and self.population_size > current_population
        force_repopulate = self.running and self.population_size > current_population * 2
        if not repopulate:
            return None
        newborn = None
        if parent1.alive and parent2.alive:
            newborn = self.crossover_member(parent1, parent2)
        elif force_repopulate:
            newborn = self.make_member()
        else:
            newborn = None
        if not newborn is None:
            self.prepare_member(newborn)
        return newborn

    def start(self):
        """
        Perform simulation startup
        """
        self.epoch = 0
        self.hyper_parameters = [c for c in self.components if c.is_hyper_parameter() ]
        self.controllers = [c for c in self.components if c.is_controller() ]

        self.outline_simulation()
        for component in self.controllers:
            component.start_simulation(self)

        self.make_initial_mutations()

        for index in range(self.population_size):
            self.make_member()
        if len(self.members) < 2:
            raise RuntimeError("Require at least 2 members to start")

        for member in self.members:
            self.prepare_member(member)

        for member in self.members:
            self.reports.append(self.record_member(member))

        members = self.members[:]
        for member in members:
            if not member.alive:
                self.bury_member(member)

        self.running = True

    def step(self):
        """
        Run a step of the simulation
        """

        if not self.running:
            raise RuntimeError("Simulation is not running")

        random_state = self.random_state
        candidates = self.members

        # If we run out of search space the population can crash.
        # Make sure we don't get into an infinite loop.
        if len(candidates) < 2:
            self.stop()
            return None

        # Pick 2 members
        contestant1, contestant2 = self.choose_competitors()

        # Make sure their evaluations are up to date
        self.evaluate_member(contestant1)
        self.evaluate_member(contestant2)

        # Have them contest.
        if contestant1.alive and contestant2.alive:
            contest = self.contest_members(contestant1, contestant2)

            # If there was no contest then something is wrong
            if contest.is_uncontested():
                raise RuntimeError("No contest component defined")

            # Determine the contestants fate!
            if contestant1.alive and contestant2.alive and contest.is_conclusive():
                self.judge_members(contestant1, contestant2, contest)

        # Repopulate!
        newborn1 = None
        newborn2 = None

        if contestant1.alive and contestant2.alive:
            newborn1 = self.repopulate(contestant1, contestant2)
            newborn2 = self.repopulate(contestant1, contestant2)

        if not contestant1.alive:
            self.bury_member(contestant1)

        if not contestant2.alive:
            self.bury_member(contestant2)

        # Report on what happened
        self.n_steps += 1
        self.reports.append(self.record_member(contestant1))
        self.reports.append(self.record_member(contestant2))
        if not newborn1 is None:
            self.reports.append(self.record_member(newborn1))
        if not newborn2 is None:
            self.reports.append(self.record_member(newborn2))

    def run(self, steps):
        """
        Run an epoch
        """
        name = "Running %s %s:" % (self.name, self.n_steps + steps)
        self.epoch += 1
        print("")
        for component in self.controllers:
            component.start_epoch(self)
        for step in range(steps):
            if not self.running:
                break
            self.step()
            printProgressBar(step, steps, prefix = name, length = 50)
        printProgressBar(steps, steps, prefix = name, length = 50)            

    def finish(self):
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
            member.finshed()

        # final report on ranked members
        for member in self.ranking.members:
            self.reports.append(self.record_member(member))

    def stop(self):
        """
        Indicate that the simulation should stop
        """
        self.running = False

    def outline_simulation(self):
        """
        Collect the simulation outline
        """
        outline = Outline()
        outline.append_attribute("simulation", Dataset.Battle, [Role.Configuration])
        for property_key in self.properties.keys():
            outline.append_attribute(property_key, Dataset.Battle, [Role.Configuration])
        outline.append_attribute("epoch", Dataset.Battle, [Role.ID])
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


        outline.append_attribute("victories", Dataset.Battle, [Role.Property])
        outline.append_attribute("defeats", Dataset.Battle, [Role.Property])
        outline.append_attribute("eliminations", Dataset.Battle, [Role.Property])
        for component in self.components:
            component.outline_simulation(self, outline)
        self.outline = outline

    def record_member(self, member):
        """
        Generate a record on a member
        """
        member_id = member.id
        epoch = self.epoch
        step = self.n_steps
        record = Record()

        record.simulation = self.name
        for property_key in self.properties.keys():
            setattr(record, property_key, self.properties[property_key])

        record.epoch = epoch
        record.step = step
        record.member_id = member_id
        record.form_id = member.form.id if member.form else None
        record.incarnation = member.incarnation
        record.event = member.event
        record.time = time.ctime(member.event_time)
        record.fault = member.fault_message

        record.rating = member.rating
        record.rating_sd = member.rating_sd
        record.ranking = member.ranking

        record.league = member.league
        record.alive = member.alive
        record.final = member.final

        record.victories = member.victories
        record.defeats = member.defeats
        record.eliminations = member.eliminations

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
