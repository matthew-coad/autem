from ..lifecycle import LifecycleManager
from ..choice import Choice
from ..evaluators.choice_evaluation import ChoiceEvaluation
from .maker import Maker

import pandas as pd
import numpy as np

class TopChoiceMaker(Maker, LifecycleManager):
    """
    Maker that prioritises the top choices using the choice model
    """

    def get_choice_evaluation(self, member):
        evaluation = member.evaluation
        if not hasattr(evaluation, "choice_evaluation"):
            evaluation.choice_evaluation = ChoiceEvaluation()
        return evaluation.choice_evaluation

    def make_grid(self, specie):
        """
        Make initial member muations list
        The initial mutation list ensures that every component choice gets selected a minimum number of times
        """

        def cross_values(grid, name, values):
            output = []
            for base in grid:
                for value in values:
                    item = {}
                    for key in base:
                        item[key] = base[key]
                    item[name] = value
                    output.append(item)
            return output

        grid = [ {} ]
        for component in specie.list_hyper_parameters():
            if isinstance(component, Choice):
                choice_names = component.get_component_names()
                grid = cross_values(grid, component.name, choice_names)
        return grid

    def evaluate_grid_predicted_scores(self, specie):

        # Get the model

        specie.set_state("initialization_grid_pred", None)

        model = specie.get_state("component_score_model")
        grid = specie.get_state("initialization_grid")

        if model is None or grid is None:
            return None

        # Build the choices into a dataframe
        choice_names = [ c.name for c in specie.list_hyper_parameters() if isinstance(c, Choice) ]
        x_values = {}
        for choice_name in choice_names:
            x_values[choice_name] = [ i[choice_name] for i in grid ]
        x = pd.DataFrame(data = x_values)

        # And do the prediction
        pred_y, pred_y_std = model.predict(x, return_std=True)

        specie.set_state("initialization_grid_pred", pred_y.tolist())

    def start_specie(self, specie):
        grid = self.make_grid(specie)
        specie.set_state("initialization_grid", grid)
        specie.set_state("initialization_grid_pred", None)

    def start_epoch(self, epoch):
        self.evaluate_grid_predicted_scores(epoch.get_specie())

    def configure_grid_member(self, specie, member, grid_index):
        grid = specie.get_state("initialization_grid")
        grid_pred = specie.get_state("initialization_grid_pred")
        grid_item = grid[grid_index]
        del grid[grid_index]

        if not grid_pred is None:
            del grid_pred[grid_index]

        for component in specie.list_hyper_parameters():
            if isinstance(component, Choice):
                component.initialize_member(member)
                component.force_member(member, grid_item[component.name])
        return True

    def configure_top_member(self, specie, member):
        grid = specie.get_state("initialization_grid")
        grid_pred = specie.get_state("initialization_grid_pred")
        grid_index = grid_pred.index(max(grid_pred))
        return self.configure_grid_member(specie, member, grid_index)

    def configure_random_member(self, member):
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        return True

    def configure_member(self, member):
        specie = member.get_specie()
        if not specie.is_spotchecking():
            return False

        grid = specie.get_state("initialization_grid")
        grid_pred = specie.get_state("initialization_grid_pred")
        if grid is None or grid_pred is None:
            return self.configure_random_member(member)
        else:
            return self.configure_top_member(specie, member)
