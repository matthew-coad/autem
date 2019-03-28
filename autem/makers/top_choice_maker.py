from .. import Maker, Member, Controller, Choice

import pandas as pd
import numpy as np

class TopChoiceMaker(Maker, Controller):
    """
    Maker that prioritises the top choices using the choice model
    """

    def make_grid(self, simulation):
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
        for component in simulation.hyper_parameters:
            if isinstance(component, Choice):
                choice_names = component.get_component_names()
                grid = cross_values(grid, component.name, choice_names)
        return grid

    def evaluate_grid_predicted_scores(self, simulation):

        # Get the model

        simulation.resources.initialization_grid_pred = None

        model = simulation.resources.component_score_model
        grid = simulation.resources.initialization_grid

        if model is None or grid is None:
            return None

        # Build the choices into a dataframe
        choice_names = [ c.name for c in simulation.hyper_parameters if isinstance(c, Choice) ]
        x_values = {}
        for choice_name in choice_names:
            x_values[choice_name] = [ i[choice_name] for i in grid ]
        x = pd.DataFrame(data = x_values)

        # And do the prediction
        pred_y, pred_y_std = model.predict(x, return_std=True)

        simulation.resources.initialization_grid_pred = pred_y.tolist()

    def start_simulation(self, simulation):
        grid = self.make_grid(simulation)
        simulation.resources.initialization_grid = grid
        simulation.resources.initialization_grid_pred = None

    def start_epoch(self, simulation):
        self.evaluate_grid_predicted_scores(simulation)

    def make_grid_member(self, simulation, grid_index):
        grid = simulation.resources.initialization_grid
        grid_pred = simulation.resources.initialization_grid_pred
        grid_item = grid[grid_index]
        del grid[grid_index]

        if not grid_pred is None:
            del grid_pred[grid_index]

        member = Member(simulation)
        for component in simulation.hyper_parameters:
            if isinstance(component, Choice):
                component.initialize_member(member)
                component.force_member(member, grid_item[component.name])
        return member

    def make_top_member(self, simulation):
        grid = simulation.resources.initialization_grid
        grid_pred = simulation.resources.initialization_grid_pred
        grid_index = grid_pred.index(max(grid_pred))
        return self.make_grid_member(simulation, grid_index)

    def make_random_member(self, simulation):
        random_state = simulation.random_state
        grid = simulation.resources.initialization_grid
        grid_index = random_state.randint(0, len(grid))
        return self.make_grid_member(simulation, grid_index)

    def make_member(self, simulation):
        grid = simulation.resources.initialization_grid
        grid_pred = simulation.resources.initialization_grid_pred
        if not grid:
            return None
        if not grid_pred is None:
            member = self.make_top_member(simulation)
        else:
            member = self.make_random_member(simulation)
        return member