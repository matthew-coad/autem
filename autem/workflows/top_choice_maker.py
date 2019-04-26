from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager
from ..member_manager import MemberManager
from ..choice import Choice
from ..evaluators.choice_evaluator import ChoiceState, get_choice_state

import pandas as pd
import numpy as np

class TopChoiceMaker(SpecieManager, EpochManager, MemberManager):
    """
    Maker that prioritises the top choices using the choice model
    """

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

        if model is None or grid is None or len(grid) == 0:
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

    def prepare_specie(self, specie):
        grid = self.make_grid(specie)
        specie.set_state("initialization_grid", grid)
        specie.set_state("initialization_grid_pred", None)

    def prepare_epoch(self, epoch):
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
        return (True, None)

    def configure_top_member(self, specie, member):
        grid = specie.get_state("initialization_grid")
        grid_pred = specie.get_state("initialization_grid_pred")
        if not grid_pred:
            return self.configure_random_member(member)

        grid_index = grid_pred.index(max(grid_pred))
        return self.configure_grid_member(specie, member, grid_index)

    def configure_random_member(self, member):
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        return (True, None)

    def configure_member(self, member):
        specie = member.get_specie()
        if specie.get_current_epoch().is_tuning():
            return (None, None)

        grid = specie.get_state("initialization_grid")
        grid_pred = specie.get_state("initialization_grid_pred")

        if grid is None or grid_pred is None:
            configured, reason = self.configure_random_member(member)
        else:
            configured, reason = self.configure_top_member(specie, member)
        if configured:
            configured, reason = member.specialize()
        return (configured, reason)

