from .. import Maker, Member, Controller, Choice
from .tune_state import TuneSpecieState

import pandas as pd
import numpy as np

class TuneMaker(Maker, Controller):
    """
    Maker that creates for tuning mode
    """

    def start_specie(self, specie):

        if not specie.is_tuning():
            return None

        simulation = specie.get_simulation()
        top_members = [ s.get_ranking().get_top_member() for s in simulation.list_species(mode = "spotcheck") if not s.get_ranking().get_top_member() is None ]
        top_members = list(reversed(sorted(top_members, key = lambda m: m.rating)))
        prototype_member = top_members[0]

        choice_components = [ c for c in specie.get_settings().get_hyper_parameters() if isinstance(c, Choice) ]
        choices = dict([ (c.name, c.get_active_component_name(prototype_member)) for c in choice_components])

        state = specie.get_resource("tune_maker", lambda: TuneSpecieState())
        state.choices = choices
        state.tuning = True
        state.prototype = prototype_member

    def configure_member(self, member):

        specie = member.get_specie()
        state = specie.get_resource("tune_maker", lambda: TuneSpecieState())
        if not state.tuning:
            return False

        prototype = state.prototype
        member.impersonate(prototype)
        return True
