from .. import Dataset, Role
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time

class Accuracy(Evaluater):
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
        performance = -duration

        if not hasattr(evaluation, "performances"):
            evaluation.performances = []

        evaluation.performances.append(performance)
        evaluation.performance = np.array(evaluation.performances).mean()

    def contest_members(self, contestant1, contestant2, outcome):

        if outcome.is_conclusive():
            return None

        required_p_value = self.p_value

        if hasattr(contestant1.evaluation, "accuracies"):
            member1_scores = np.array(contestant1.evaluation.accuracies)
        else:
            member1_scores = []

        if hasattr(contestant2.evaluation, "accuracies"):
            member2_scores = np.array(contestant2.evaluation.accuracies)
        else:
            member2_scores = []

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            outcome.inconclusive()
            return None

        # Run the t-test
        try:
            test_result = stats.ttest_ind(member1_scores, member2_scores)
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
            outcome.inconclusive()
            return None

        # Determine the victor
        if t_statistic > 0:
            victor = 1
        else:
            victor = 2

        decisive = maturity < required_p_value / 2
        
        if decisive:
            outcome.decisive(victor)
        else:
            outcome.indecisive(victor)

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "accuracy"):
            record.accuracy = evaluation.accuracy
        else:
            record.accuracy = None
