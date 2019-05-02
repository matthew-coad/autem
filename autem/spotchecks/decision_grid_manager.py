from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager
from ..member_manager import MemberManager
from ..choice import Choice

from ..component_state import ComponentState
from .decision_grid_state import DecisionGridState
from .decision_state import DecisionState

import pandas as pd
import numpy as np

class DecisionGridManager(SpecieManager, EpochManager, MemberManager):
    """
    Provides services for the management and creation of decision grids.
    """

    def build_decision_grid(self, specie):
        """
        Build a decision grid
        """

        def cross_values(grid, name, values):
            output = []
            for base in grid:
                base_decision = base.get_decision()
                for value in values:
                    decision = {}
                    for key in base_decision:
                        decision[key] = base_decision[key]
                    decision[name] = value
                    output.append(DecisionState(decision))
            return output

        grid = [ DecisionState({}) ]
        components = ComponentState.get(specie)
        choices = components.list_choices()
        for choice in choices:
            options = components.list_options(choice)
            option_values = [ o.get_name() for o in options ]
            grid = cross_values(grid, choice.get_name(), option_values)
        return grid

    def prepare_specie(self, specie):
        grid = self.build_decision_grid(specie)
        state = DecisionGridState.get(specie)
        state.initialize(grid)
