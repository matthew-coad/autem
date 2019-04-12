from .. import Dataset, Role, WarningInterceptor, Choice
from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation
from .choice_evaluation import ChoiceEvaluation

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

class ChoiceEvaluator(Evaluater):
    """
    Component that performs evaluations related to choices
    """

    def __init__(self):
        pass

    def get_score_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "score_evaluation"):
            evaluation.score_evaluation = ScoreEvaluation()
        return evaluation.score_evaluation

    def get_choice_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "choice_evaluation"):
            evaluation.choice_evaluation = ChoiceEvaluation()
        return evaluation.choice_evaluation

    def build_member_score_df(self, specie):
        """
        Build a dataframe containing all scores evaluated for each member
        """

        # Collect all members including ones from the graveyard which have scores
        # Not concerned whether they failed or not or whether they were reincarnated
        # Just get as much information as we have
        all_members = [ m for m in specie.list_members(graveyard = True )  if self.get_score_evaluation(m).scores ]

        if not all_members:
            return None

        # Get all the choices
        choices = [ c for c in specie.get_settings().get_hyper_parameters() if isinstance(c, Choice) ]

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
        scores = [(m.id, s) for m in all_members for s in self.get_score_evaluation(m).scores ]
        score_df = pd.DataFrame(scores, columns=['member_id', 'score'])

        # Join the frames together
        member_score_df = pd.merge(choice_df, score_df, on='member_id', how='inner')

        # Determine mean score per component group
        choice_names = [ c.name for c in choices ]
        member_score_df = member_score_df.groupby(choice_names, as_index=False).agg({"score": "mean"})
        return member_score_df

    def build_model(self, specie):

        # Get the data
        df = self.build_member_score_df(specie)
        if df is None:
            return None

        # Extract the choices as the response variables
        choices = [ c for c in specie.get_settings().get_hyper_parameters() if isinstance(c, Choice) ]
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

    def evaluate_model(self, specie):

        # Build the model
        model = self.build_model(specie)
        specie.get_resources().component_score_model = model

        # Reset the expected score for all members
        for member in specie.list_members():
            member.evaluation.choice_evaluation = ChoiceEvaluation()

    def build_predicted_score(self, member):
        """
        Evaluate the expected score for a member
        """

        # Get the model
        specie = member.get_specie()
        model = specie.get_resources().component_score_model
        if model is None:
            return (None, None)

        # Build the choices into a dataframe
        choices = [ c for c in specie.get_settings().get_hyper_parameters() if isinstance(c, Choice) ]
        choice_values = dict([ (c.name, [c.get_active_component_name(member)]) for c in choices])
        x = pd.DataFrame(choice_values)

        # And do the prediction
        pred_y, pred_y_std = model.predict(x, return_std=True)
        return (pred_y[0], pred_y_std[0])

    def evaluate_member(self, member):

        choice_evaluation = self.get_choice_evaluation(member)
        if not choice_evaluation.choice_predicted_score is None:
            return None

        choice_predicted_score, choice_predicted_score_std = self.build_predicted_score(member)
        choice_evaluation.choice_predicted_score = choice_predicted_score
        choice_evaluation.choice_predicted_score_std = choice_predicted_score_std

    def start_epoch(self, epoch):
        self.evaluate_model(epoch.get_specie())

    def record_member(self, member, record):
        super().record_member(member, record)

        choice_evaluation = self.get_choice_evaluation(member)
        record.CE_score = choice_evaluation.choice_predicted_score
        record.CE_score_std = choice_evaluation.choice_predicted_score_std
