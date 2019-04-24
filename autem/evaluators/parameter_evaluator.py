from .evaluator import Evaluater
from .score_evaluator import ScoreState
from .parameter_state import ParameterEvaluation, get_parameter_evaluation, set_parameter_evaluation, ParameterModel, ParameterModelResources, get_parameter_models

import numpy as np
import pandas as pd

from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold
from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as kernels
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

import warnings
import time

class ParameterEvaluator(Evaluater):
    """
    Component that performs predictions related to hyperparameters
    """

    def __init__(self):
        pass

    def get_source_members(self, specie):
        # Collect all members including ones from the graveyard and from previous species
        # Just as long as they have scores
        combined_members = [ m for s in specie.get_simulation().list_species() for m in s.list_members(buried = True) if not get_score_evaluation(m).score is None ] 
        return combined_members

    def get_choice_components(self, specie):
        choice_components = [ c for c in specie.list_hyper_parameters() if isinstance(c, Choice) ]
        return choice_components

    def get_parameter_components(self, specie, choices):
        parameter_components = [ p for c in self.get_choice_components(specie) for p in c.get_component(choices[c.name]).parameters ]
        return parameter_components

    def build_member_score_df(self, specie, choices):
        """
        Build a dataframe containing scores evaluated for each member that used the given choices
        """

        members = self.get_source_members(specie)
        if not members:
            return None

        # Get the components
        choice_components = self.get_choice_components(specie)
        parameter_components = self.get_parameter_components(specie, choices)

        # Determine if a members choices match the given ones
        def choices_match(member):
            match = True
            for component in choice_components:
                match = match and component.get_active_component_name(member) == choices[component.name]
            return match
        members = [ m for m in members if choices_match(m) ]
        if not members:
            return None

        # Build a frame containing for each member its parameters
        member_parameters = {
            "member_id": [ m.id for m in members ]
        }
        for parameter in parameter_components:
            member_parameters[parameter.get_record_name()] = [ parameter.get_value(m) for m in members ]
        parameter_df = pd.DataFrame(member_parameters)

        # Build a frame containing fit score for each member
        scores = [(m.id, get_score_evaluation(m).score) for m in members ]
        score_df = pd.DataFrame(scores, columns=['member_id', 'score'])

        # Join the frames together
        member_score_df = pd.merge(parameter_df, score_df, on='member_id', how='inner')

        # Determine mean score per parameter
        # But in general they should be pretty much the same
        parameter_names = [ p.get_record_name() for p in parameter_components ]
        group_df = member_score_df.groupby(parameter_names, as_index=False).agg({"score": "mean"})
        return group_df

    def build_model(self, specie, choices):

        # Get the data
        df = self.build_member_score_df(specie, choices)
        if df is None or df.shape[0] < 5:
            return None

        # Extract the parameters as the response variables
        contribution_count = df.shape[0]
        parameters = self.get_parameter_components(specie, choices)
        parameter_names = [ p.get_record_name() for p in parameters ]
        x = df.loc[:, parameter_names]

        # Extract the scores as the dependant variables
        y = df.loc[:, "score"]

        categorical_features = [ i for i in range(len(parameters)) if parameters[i].type == 'nominal' ]
        numeric_features = [ i for i in range(len(parameters)) if parameters[i].type == 'numeric' ]

        categories = []
        for feature in categorical_features:
            values = parameters[feature].choices
            values = np.sort(values)
            categories.append(values)

        # We create the preprocessing pipelines for both numeric and categorical data.
        # numeric_features = [0, 1, 2, 5, 6]
        numeric_scaler = StandardScaler()
        numeric_transformer = numeric_scaler

        # categorical_features = [3, 4, 7, 8]
        categorical_encoder = OneHotEncoder(categories=categories, dtype = np.float64, handle_unknown = "error", sparse=False)
        categorical_transformer = categorical_encoder

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])

        # Define the isotropic kernel
        kernel = 1.0 * kernels.RBF() + kernels.WhiteKernel()

        # Define the regressor
        regressor = GaussianProcessRegressor(kernel=kernel, normalize_y = True)

        # Build the pipeline and fit it
        pipeline = Pipeline(steps = [
            ('prep', preprocessor),
            ('regressor', regressor)
        ])

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                pipeline.fit(x, y)
            except Exception as ex:
                return None
        return ParameterModel(pipeline, contribution_count)

    def evaluate_model(self, specie, choices):

        # Get the cached model
        models = get_parameter_models(specie).models
        model_key = str(choices)
        model = None
        if model_key in models:
            model = models[model_key]

        if model is None:
            model = self.build_model(specie, choices)
            if not model is None:
                models[model_key] = model
        return model

    def build_predicted_score(self, member, choices):
        """
        Evaluate the expected score for a member
        """

        # Get the model
        specie = member.get_specie()
        parameter_model = self.evaluate_model(specie, choices)
        parameter_evaluation = ParameterEvaluation()
        if parameter_model is None:
            return parameter_evaluation

        # Build the parmaeters into a data from
        parameters = self.get_parameter_components(specie, choices)
        parameter_values = dict([ (p.get_record_name(), [ p.get_value(member) ] ) for p in parameters])
        x = pd.DataFrame(parameter_values)

        # And do the prediction
        pred_y, pred_y_std = parameter_model.model.predict(x, return_std=True)
        parameter_evaluation.predicted_score = pred_y[0]
        parameter_evaluation.predicted_score_std = pred_y_std[0]
        parameter_evaluation.contribution_count = parameter_model.contribution_count
        return parameter_evaluation

    def evaluate_member(self, member):

        parameter_evaluation = get_parameter_evaluation(member)
        if not parameter_evaluation.predicted_score is None:
            return None

        specie = member.get_specie()
        choice_components = self.get_choice_components(specie)
        choices = dict([ (c.name, c.get_active_component_name(member)) for c in choice_components])

        parameter_evaluation = self.build_predicted_score(member, choices)
        set_parameter_evaluation(member, parameter_evaluation)

    def prepare_epoch(self, epoch):
        # Force all score models to be recalculated at the start of every epoch
        specie = epoch.get_specie()
        get_parameter_models(specie).score_models = {}

    def record_member(self, member, record):
        super().record_member(member, record)

        parameter_evaluation = get_parameter_evaluation(member)

        record.PE_score = parameter_evaluation.predicted_score
        record.PE_score_std = parameter_evaluation.predicted_score_std
        record.PE_contributions = parameter_evaluation.contribution_count
