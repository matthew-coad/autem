from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time

class AccuracyContest(Evaluater):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def evaluate_member(self, member):
        super().evaluate_member(member)

        simulation = member.simulation
        resources = member.resources
        evaluation = member.evaluation
        random_state = simulation.random_state

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        start = time.time()

        x,y = loader.load_training_data(simulation)
        test_size = 0.2
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

        pipeline = resources.pipeline
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)

        accuracy = scorer.score(y_test, y_pred)
        if not hasattr(evaluation, "accuracies"):
            evaluation.accuracies = []

        evaluation.accuracies.append(accuracy)
        evaluation.accuracy = np.array(evaluation.accuracies).mean()

        end = time.time()
        duration = end - start

        if not hasattr(evaluation, "durations"):
            evaluation.durations = []

        evaluation.duration = duration
        evaluation.durations.append(duration)

    def contest_members(self, contestant1, contestant2, outcome):

        required_p_value = self.p_value
        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        if outcome.is_conclusive():
            return None

        if hasattr(contestant1.evaluation, "accuracies"):
            contestant1_accuracies = np.array(contestant1.evaluation.accuracies)
            contestant1_accuracy = contestant1.evaluation.accuracy
        else:
            contestant1_accuracies = []
            contestant1_accuracy = None

        if hasattr(contestant2.evaluation, "accuracies"):
            contestant2_accuracies = np.array(contestant2.evaluation.accuracies)
            contestant2_accuracy = contestant2.evaluation.accuracy
        else:
            contestant2_accuracies = []
            contestant2_accuracy = None

        # Record the accuracies each member has encountered so we can assess decisiveness in later contests
        if not contestant2_accuracy is None:
            if not hasattr(contestant1.evaluation, "accuracies_encountered"):
                contestant1.evaluation.accuracies_encountered = []
            contestant1.evaluation.accuracies_encountered.append(contestant2_accuracy)

        if not contestant1_accuracy is None:
            if not hasattr(contestant2.evaluation, "accuracies_encountered"):
                contestant2.evaluation.accuracies_encountered = []
            contestant2.evaluation.accuracies_encountered.append(contestant1_accuracy)

        # Must have at least 3 scores each to make a comparison
        if len(contestant1_accuracies) < 3 or len(contestant2_accuracies) < 3:
            outcome.inconclusive()
            return None

        # Run the t-test
        try:
            test_result = stats.ttest_ind(contestant1_accuracies, contestant2_accuracies)
        except:
            outcome.inconclusive()
            return None

        t_statistic = test_result[0] # positive if 1 > 2
        maturity = test_result[1]
        mature = 1 if maturity <= required_p_value else 0

        contestant1.maturing(maturity, mature)
        contestant2.maturing(maturity, mature)

        # Need at least the required p-value to have an outcome
        if maturity > required_p_value:
            contestant1.evaluation.accuracy_contest = "Inconclusive"
            contestant2.evaluation.accuracy_contest = "Inconclusive"
            outcome.inconclusive()
            return None

        # Determine the victor
        if t_statistic > 0:
            victor = 1
        else:
            victor = 2

        victorious_contestant = contestant1 if victor == 1 else contestant2
        defeated_contestant = contestant2 if victor == 1 else contestant1

        # Determine decisiveness. A victory is decisive if its in the top half of the accuracies that each
        # member has encountered

        victorious_encounters = victorious_contestant.evaluation.accuracies_encountered
        defeated_encounters = defeated_contestant.evaluation.accuracies_encountered
        max_encounters = max(len(victorious_encounters), len(defeated_encounters))
        victorious_encounters = victorious_encounters[-max_encounters:]
        defeated_encounters = defeated_encounters[-max_encounters:]

        encounter_cutoff = defeated_contestant.evaluation.accuracy
        encounters = [ e for e in victorious_encounters + defeated_encounters if e >= encounter_cutoff ]
        decisive_cutoff = np.percentile(encounters, 55)
        decisive = victorious_contestant.evaluation.accuracy >= decisive_cutoff
        
        if decisive:
            victorious_contestant.evaluation.accuracy_contest = "Victory"
            defeated_contestant.evaluation.accuracy_contest = "Defeat"
            outcome.decisive(victor)
        else:
            victorious_contestant.evaluation.accuracy_contest = "Win"
            defeated_contestant.evaluation.accuracy_contest = "Loss"
            outcome.indecisive(victor)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "accuracy"):
            record.accuracy = evaluation.accuracy
        else:
            record.accuracy = None

        evaluation = member.evaluation
        if hasattr(evaluation, "duration"):
            record.duration = evaluation.duration
        else:
            record.duration = None

        if hasattr(evaluation, "accuracy_contest"):
            record.accuracy_contest = evaluation.accuracy_contest
        else:
            record.accuracy_contest = None
