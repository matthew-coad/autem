
from .rater import Rater
import openml

import numpy as np
from scipy import stats

class OpenMLRater(Rater):
    """
    Rates a model by using an openml task
    """

    def __init__(self, task_id):
        Rater.__init__(self, "OpenMLRater")
        self.task_id = task_id

    def start_simulation(self, simulation):
        super().start_simulation(simulation)
        task_id = self.task_id
        task = openml.tasks.get_task(task_id)
        simulation.resources.task = task

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only mature, attractive members get a rating.
        """
        if not member.rating is None:
            # Don't rerate! It's expensive
            return None

        simulation = member.simulation
        task = simulation.resources.task 
        pipeline = member.preparations.pipeline

        run = openml.runs.run_model_on_task(task, pipeline)
        predictive_accuracy = run.fold_evaluations['predictive_accuracy']
        scores = np.array([score for rep, folds in predictive_accuracy.items() for fold, score in folds.items()])

        rating = scores.mean()
        rating_sd = scores.std()

        member.ratings.predictive_accuracy = rating
        member.ratings.predictive_accuracy_sd = rating_sd

        member.rated(rating)
