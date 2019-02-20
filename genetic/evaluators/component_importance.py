from .evaluator import Evaluater
from ..simulators import Choice

import pandas as pd
import numpy as np
from scipy import stats
from collections import defaultdict

from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import ExtraTreesRegressor

class ComponentImportance(Evaluater):
    """
    Evaluates the importance of each component choice using RandomForest
    """

    def start_simulation(self, simulation):
        """
        At the start of the simulation create a dataframe used to track the data needed to evaluate
        component choices
        """

        super().start_simulation(simulation)

        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice) ]
        if not choices:
            return None

        columns = [ (c.name, []) for c  in choices ]
        columns.append(("accuracy", []))
        df_empty = pd.DataFrame(dict(columns))

        simulation.resources.choice_importance_data = df_empty

    def evaluate_member(self, member):
        """
        After each member evaluation keep the component accuracy data
        """
        super().evaluate_member(member)

        simulation = member.simulation
        if not hasattr(simulation.resources, "choice_importance_data"):
            return None

        choices = [ c for c in simulation.hyper_parameters if isinstance(c, Choice) ]
        columns = [ (c.name, c.get_active_component_name(member)) for c in choices ]
        columns.append(("accuracy", member.evaluation.accuracy))

        df = simulation.resources.choice_importance_data.append(dict(columns), ignore_index=True)
        simulation.resources.choice_importance_data = df

