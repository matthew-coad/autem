from .evaluator import Evaluater

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
    Evaluates the importance of each component using RandomForest
    """

    def __init__(self):
        """
        P value used to determine if the scores are significantly different
        """
        Evaluater.__init__(self, "ComponentImportance")

    def start_simulation(self, simulation):
        """
        At the start of the simulation create a dataframe used to track the data needed to evaluate
        importance
        """

        super().start_simulation(simulation)

        components = [ c for c in simulation.components if c.is_mutator() ]
        columns = [ (p.get_record_name(c), []) for c in components for p in c.parameters ]
        columns.append(("accuracy", []))
        df_empty = pd.DataFrame(dict(columns))

        simulation.resources.component_importance_data = df_empty

    def evaluate_member(self, member):
        """
        After each member evaluation keep the component accuracy data
        """

        super().evaluate_member(member)

        simulation = member.simulation
        components = [ c for c in simulation.components if c.is_mutator() ]
        columns = [ (p.get_record_name(c), p.get_value(member ) ) for c in components if c.is_active(member) for p in c.parameters ]
        columns.append(("accuracy", member.evaluation.accuracy))

        df = simulation.resources.component_importance_data.append(dict(columns), ignore_index=True)
        simulation.resources.component_importance_data = df

    def start_epoch(self, simulation):
        """
        At the start of the epoch fit a random forest model to determine variable importance
        """

        component_importance_data = simulation.resources.component_importance_data
        if component_importance_data.shape[0] == 0:
            # No data so don't bother
            return

        df = component_importance_data.copy()
        column_names = list(df.columns)
        text_columns = list(df.columns[df.dtypes == np.object])
        float_columns = list(df.columns[df.dtypes == np.float64])
        for column in text_columns:
            df[column] = np.where(df[column].isnull(), "None", df[column])
        for column in float_columns:
            some_missing = any(df[column].isnull())
            if some_missing:
                missing_column = "%s|Missing" % column
                df[missing_column] = np.where(df[column].isnull(), 1, 0)
                df[column] = np.where(df[column].isnull(), 0, df[column])
        x = pd.get_dummies(df[df.columns[df.columns != "accuracy"]], prefix_sep="|")
        y = df["accuracy"]
        learner = ExtraTreesRegressor()
        learner.fit(x, y)

        def decode_column(index):
            name = x.columns[index]
            importance = learner.feature_importances_[index]
            parts1 = name.split('|', 1)
            parts2 = parts1[0].split('_', 1)
            component = parts2[0]
            parameter = parts2[1]
            category = parts1[1] if len(parts1) == 2 else None
            return {"combined": name, "component": component, "parameter": parameter, "category": category, "importance": importance}

        component_parameter_importance = [ decode_column(index) for index in range(len(x.columns))]
        component_importance_dict = defaultdict(lambda: {"importance": 0, "parameters": list()})
        for parameter_importance in component_parameter_importance:
            component = parameter_importance["component"]
            component_importance = component_importance_dict[component]
            component_importance["importance"] += parameter_importance["importance"]
            component_importance["parameters"].append(parameter_importance)
        
        simulation.resources.component_parameter_importance = component_parameter_importance
        simulation.resources.component_importances = component_importance_dict

        a = 1
