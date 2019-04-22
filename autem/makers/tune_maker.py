from .. import Maker, Member, LifecycleManager, Choice

import pandas as pd
import numpy as np

class TuneSpecieState():

    """
    Tune specie state
    """
    def __init__(self):
        self.tuning = False
        self.choices = None
        self.prototype = None

class TuneMaker(Maker, LifecycleManager):
    """
    Maker that creates the tuning model
    """

    def start_specie(self, specie):

        if not specie.is_tuning():
            return None

        simulation = specie.get_simulation()
        top_members = [ s.get_ranking().get_top_member() for s in simulation.list_species(mode = "spotcheck") if not s.get_ranking().get_top_member() is None ]
        top_members = list(reversed(sorted(top_members, key = lambda m: m.rating)))
        prototype_member = top_members[0]

        choice_components = [ c for c in specie.list_hyper_parameters() if isinstance(c, Choice) ]
        choices = dict([ (c.name, c.get_active_component_name(prototype_member)) for c in choice_components])

        state = specie.get_state("tune_maker", lambda: TuneSpecieState())
        state.choices = choices
        state.tuning = True
        state.prototype = prototype_member

    def configure_member(self, member):

        specie = member.get_specie()
        state = specie.get_state("tune_maker", lambda: TuneSpecieState())
        if not state.tuning:
            return False

        prototype = state.prototype
        member.impersonate(prototype)
        return True
