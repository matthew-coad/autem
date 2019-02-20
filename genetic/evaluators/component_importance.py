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

    def start_epoch(self, simulation):
        """
        At the start of the epoch fit a to determine component choice importance
        """
        if not hasattr(simulation.resources, "choice_importance_data"):
            return None

        choice_importance_data = simulation.resources.choice_importance_data
        if choice_importance_data.shape[0] == 0:
            # No data yet so don't bother
            return

        df = choice_importance_data.copy()
        x = df[df.columns[df.columns != "accuracy"]]
        x = pd.get_dummies(x, prefix_sep="|")
        y = df["accuracy"]
        learner = ExtraTreesRegressor(n_estimators=10)
        learner.fit(x, y)

        def decode_column(index):
            name = x.columns[index]
            importance = learner.feature_importances_[index]
            parts1 = name.split('|', 1)
            choice = parts1[0]
            component = parts1[1]
            return {"combined": name, "choice": choice, "component": component, "importance": importance}

        choice_importance_details = [ decode_column(index) for index in range(len(x.columns))]
        choice_importances = defaultdict(lambda: {"importance": 0, "details": list()})
        for detail in choice_importance_details:
            choice = detail["choice"]
            choice_importance = choice_importances[choice]
            choice_importance["importance"] += detail["importance"]
            choice_importance["details"].append(detail)

        simulation.resources.choice_importances = choice_importances

    def record_member(self, member, record):
        simulation = member.simulation
        if not hasattr(simulation.resources, "choice_importances"):
            return None
        choice_importances = simulation.resources.choice_importances

        for key in choice_importances:
            setattr(record, "%s_importance" % key, choice_importances[key]["importance"])
