
from .evaluator import Evaluater

import openml

import numpy as np
from scipy import stats
import warnings

class OpenMLRater(Evaluater):
    """
    Rates model
    """

    def __init__(self, task_id):
        self.task_id = task_id

    def prepare_simulation(self, simulation):
        super().prepare_simulation(simulation)
        task_id = self.task_id
        task = openml.tasks.get_task(task_id)
        simulation.get_simulation_resources().task = task

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """
        if not member.rating is None:
            # Don't rerate! It's expensive
            return None

        task = member.get_simulation_resources().task 
        pipeline = member.get_member_resources().pipeline

        try:
            run = openml.runs.run_model_on_task(task, pipeline)
        except Exception as ex:
            member.fail(ex, "rate_member", "OpenMLRater")
            return None
            
        predictive_accuracy = run.fold_evaluations['predictive_accuracy']
        scores = np.array([score for rep, folds in predictive_accuracy.items() for fold, score in folds.items()])

        rating = scores.mean()
        rating_sd = scores.std()

        member.rated(rating, rating_sd)
