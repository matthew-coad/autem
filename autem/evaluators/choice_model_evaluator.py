from .. import Dataset, Role, WarningInterceptor, Choice
from .evaluator import Evaluater

import numpy as np
import pandas as pd

from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold
from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as kernels
from sklearn.preprocessing import OneHotEncoder

import warnings
import time

class ChoiceModelEvaluator(Evaluater):
    """
    Component that evaluates the choice model
    """

    def __init__(self):
        pass

    def build_member_score_df(self, simulation):
        """
        Build a dataframe containing all scores evaluated for each member
        """

        # Collect all members including ones from the graveyard which have scores
        # Not concerned whether they failed or not or whether they were reincarnated
        # Just get as much information as we have
        all_members = [ m for m in simulation.members + simulation.graveyard if hasattr(m.evaluation, "scores") ]

        if not all_members:
            return None

        # Get all the choices
        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice) ]

        # Build a frame containing for each member all the choices
        def get_choice_values(choice):
            values = [ choice.get_active_component_name(m) for m in all_members ]
            return values
        member_choices = {
            "member_id": [ m.id for m in all_members ]
        }
        for choice in choices:
            member_choices[choice.name] = get_choice_values(choice)
        choice_df = pd.DataFrame(member_choices)

        # Build a frame containing all fit scores for each member
        scores = [(m.id, s) for m in all_members for s in m.evaluation.scores ]
        score_df = pd.DataFrame(scores, columns=['member_id', 'score'])

        # Join the frames together
        member_score_df = pd.merge(choice_df, score_df, on='member_id', how='inner')

        # Determine mean score per component group
        choice_names = [ c.name for c in choices ]
        member_score_df = member_score_df.groupby(choice_names, as_index=False).agg({"score": "mean"})
        return member_score_df

    def build_model(self, simulation):

        # Get the data
        df = self.build_member_score_df(simulation)
        if df is None:
            return None

        # Extract the choices as the response variables
        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice) ]
        choice_names = [ c.name for c in choices ]
        x = df.loc[:, choice_names]

        # Extract the scores as the dependant variables
        y = df.loc[:, "score"]

        # Preprocess using one hot encoding
        categories = [ c.get_component_names() for c in choices ]
        encoder = OneHotEncoder(sparse = False, categories = categories)

        # Define the isotropic kernel
        kernel = 1.0 * kernels.RBF([5]) + kernels.WhiteKernel()

        # Define the regressor
        regressor = GaussianProcessRegressor(kernel=kernel, normalize_y = True)

        # Build the pipeline and fit it
        pipeline = Pipeline(steps = [
            ('encoder', encoder),
            ('regressor', regressor)
        ])
        pipeline.fit(x, y)

        return pipeline

    def start_epoch(self, simulation):

        # Build the model
        model = self.build_model(simulation)
        simulation.resources.component_score_model = model

        # Reset the expected score for all members
        for member in simulation.members:
            member.evaluation.choice_predicted_score = None
            member.evaluation.choice_predicted_score_std = None

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "choice_predicted_score"):
            record.choice_predicted_score = evaluation.choice_predicted_score
            record.choice_predicted_score_std = evaluation.choice_predicted_score_std
        else:
            record.choice_predicted_score = None
