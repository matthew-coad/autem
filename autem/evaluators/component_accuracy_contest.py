from .. import Choice
from .evaluator import Evaluater

import numpy as np
from scipy import stats

import time
from collections import defaultdict

class ComponentAccuracyContest(Evaluater):
    """
    Contest that selects the member that uses the most accurate components
    """
    def __init__(self, p_value = 0.05):
        """
        P value used to determine if the accuracies are significantly different
        """
        self.p_value = p_value

    def start_simulation(self, simulation):
        component_stats = defaultdict(lambda: {"accuracies": []})
        simulation.resources.component_stats = component_stats

    def start_epoch(self, simulation):
        """
        At the start of the epoch fit collect the stats we need to run the component accuracy contest
        """
        super().start_epoch(simulation)

        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice)]
        component_stats = simulation.resources.component_stats
        component_stats.clear()

        # Iterate through all members, including those in the graveyard
        # If that member used a component, record the accuracy and duration in the component stats

        def accumulate_member_choice(member, choice):
            choice_name = choice.name
            component_name = choice.get_active_component_name(member)
            stat_key = (choice_name, component_name)
            component_stats[stat_key]["accuracies"].append(member.evaluation.accuracy)

        target_members = simulation.members + simulation.graveyard
        for member in target_members:
            if hasattr(member.evaluation, "accuracy"):
                for choice in choices:
                    accumulate_member_choice(member, choice)

    def contest_members(self, contestant1, contestant2, outcome):
        """
        To perform the component accuracy contest we check the accuracy history of each
        component and determine the outcome based on if there is a significant difference 
        """
        if outcome.is_conclusive():
            return None

        simulation = contestant1.simulation
        required_p_value = self.p_value
        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice)]
        component_stats = simulation.resources.component_stats
        contestant1.evaluation.component_accuracy_contest = None
        contestant2.evaluation.component_accuracy_contest = None

        def accuracy_contest(choice):

            # No contest if we already have a conclusion
            if outcome.is_conclusive():
                return None

            # Get the component selected by each member
            member1_component_name = choice.get_active_component_name(contestant1)
            member2_component_name = choice.get_active_component_name(contestant2)

            # No contest if they are the same
            if member1_component_name == member2_component_name:
                return None

            # Collect the accuracies
            member1_key = (choice.name, member1_component_name)
            member1_accuracies = component_stats[member1_key]["accuracies"]

            member2_key = (choice.name, member2_component_name)
            member2_accuracies = component_stats[member2_key]["accuracies"]

            # Must have at least 20 scores each to make a comparison
            if len(member1_accuracies) < 20 or len(member2_accuracies) < 20:
                return None

            contestant1.evaluation.component_accuracy_contest = "Standoff"
            contestant2.evaluation.component_accuracy_contest = "Standoff"

            # Run the t-test to see if one component is better than the other
            try:
                test_result = stats.ttest_ind(member1_accuracies, member2_accuracies)
            except:
                outcome.inconclusive()
                return None

            t_statistic = test_result[0] # positive if 1 > 2
            p_value = test_result[1]

            if p_value <= required_p_value:
                if t_statistic > 0:
                    victor = 1
                    contestant1.evaluation.component_accuracy_contest = "%s victory" % choice.name
                    contestant2.evaluation.component_accuracy_contest = "%s defeat" % choice.name
                else:
                    victor = 2
                    contestant1.evaluation.component_accuracy_contest = "%s defeat" % choice.name
                    contestant2.evaluation.component_accuracy_contest = "%s victory" % choice.name
                outcome.decisive(victor)
                return None

            if choice.no_choice is None:
                return None

            # Run the Kolmogorov-Smirnov Test to see if both values are the same
            try:
                same_result = stats.ks_2samp(member1_accuracies, member2_accuracies)
            except:
                outcome.inconclusive()
                return None

            same_statistic = same_result[0]
            same_p_value = same_result[1]

            if same_p_value <= required_p_value:
                # The distributions are basically the same
                # If one is a no-choice then it wins
                victor = None
                if member1_component_name == choice.no_choice.name:
                    victor = 1
                    contestant1.evaluation.component_accuracy_contest = "%s no choice" % choice.name
                    contestant2.evaluation.component_accuracy_contest = "%s irrelevant" % choice.name
                elif member2_component_name == choice.no_choice.name:
                    victor = 2
                    contestant1.evaluation.component_accuracy_contest = "%s irrelevant" % choice.name
                    contestant2.evaluation.component_accuracy_contest = "%s no choice" % choice.name

                if not victor is None:
                    outcome.indecisive(victor)
                return None

            return None
        
        # Evaluate contest for each choice
        for choice in choices:
            accuracy_contest(choice)

        # If we couldn't find out anything make sure we tell the 
        # simulation that we did check
        if outcome.is_uncontested():
            outcome.inconclusive()

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "component_accuracy_contest"):
            record.compacc_contest = evaluation.component_accuracy_contest
        else:
            record.compacc_contest = None
