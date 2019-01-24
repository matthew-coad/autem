from .components import Component
from . import members
from . import populations
from . import contests

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import get_scorer
from sklearn.pipeline import Pipeline

from scipy import stats

class Data(Component):
    """
    Defines data for a model solver
    """

    def __init__(self, x, y, test_size):
        self.x = x
        self.y = y
        self.test_size = test_size

    def initializePopulation(self, population):
        population.configuration.x = self.x
        population.configuration.y = self.y
        population.configuration.test_size = self.test_size

    def evaluatePopulation(self, population):
        random_state = population.simulation.random_state
        x = population.configuration.x
        y = population.configuration.y
        test_size = population.configuration.test_size
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
        population.evaluation.x_train = x_train
        population.evaluation.x_test = x_test
        population.evaluation.y_train = y_train
        population.evaluation.y_test = y_test


class ModelChoice(Component):

    def __init__(self, models):
        self.models = models

    def initializeMember(self, member):
        random_state = member.simulation.random_state
        model_index = random_state.randint(0, len(self.models))
        member.configuration.model_index = model_index

    def copyMember(self, member, parent0):
        member.configuration.model_index = parent0.configuration.model_index

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.model_index = parent0.configuration.model_index

    def evaluateMember(self, member):
        model_index = member.configuration.model_index
        model = self.models[model_index]
        member.evaluation.model_name = model[0]
        member.evaluation.model = model[1]

    def reportMember(self, member, row):
        row.model_dim = member.evaluation.model_name

class ModelScorer(Component):
    """
    Component that evaluates model scores
    """

    def __init__(self, scorer):
        self.scorer = scorer

    def initializeMember(self, member):
        member.history.model_scores = []

    def copyMember(self, member, parent0):
        member.history.model_scores = parent0.evaluation.model_scores[:]

    def crossoverMember(self, member, parent0, parent1):
        member.history.model_scores = []

    def evaluateMember(self, member):

        model = member.evaluation.model
        model_name = member.evaluation.model_name
        population = member.population
        if hasattr(member.evaluation, "steps"):
            steps = member.evaluation.steps
        else:
            steps = []
        steps.append((model_name, model))
        pipeline = Pipeline(steps=steps)
        scorer = self.scorer

        x_train = population.evaluation.x_train
        y_train = population.evaluation.y_train
        x_test = population.evaluation.x_test
        y_test = population.evaluation.y_test

        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)
        model_score = scorer(y_test, y_pred)
        model_scores = member.history.model_scores
        model_scores.append(model_score)

        member.evaluation.model_score = model_score
        member.evaluation.model_scores = model_scores
        member.evaluation.model_p_value = 1

    def reportMember(self, member, row):
        row.n_fit_measure = len(member.evaluation.model_scores)
        row.p_value_measure = member.evaluation.model_p_value
        row.score_kpi = np.mean(member.evaluation.model_scores)

class ModelScoreFitness(Component):
    """
    Fitness is just the highest model score
    """
    def battleMembers(self, population, member1, member2):
        if member1.evaluation.model_score > member2.evaluation.model_score:
            return 1
        elif member1.evaluation.model_score < member2.evaluation.model_score:
            return 2
        else:
            return 0

class ModelScoreSignificantFitness(Component):
    """
    Determines fitness by comparing mean model scores but only
    if the difference is considered significant
    """

    def __init__(self, p_value = 0.1):
        """
        P value used to determine if the scores are significantly different
        """
        self.p_value = p_value

    def battleMembers(self, population, member1, member2):

        member1_scores = member1.evaluation.model_scores
        member2_scores = member2.evaluation.model_scores
        required_p_value = self.p_value

        # Must have at least 3 scores each to make a comparison
        if len(member1_scores) < 3 or len(member2_scores) < 3:
            return 0

        # Run the t-test
        test_result = stats.ttest_ind(member1_scores, member2_scores)
        t_statistic = test_result[0] # positive if 1 > 2
        p_value = test_result[1]

        # Record the best p-value for each model
        if member1.evaluation.model_p_value > p_value:
            member1.evaluation.model_p_value  = p_value
        if member2.evaluation.model_p_value > p_value:
            member2.evaluation.model_p_value  = p_value

        # Need at least the required p-value
        if p_value > required_p_value:
            return 0

        if t_statistic > 0:
            return 1
        else:
            return 2
