from ..epoch_manager import EpochManager
from ..member_manager import MemberManager
from ..choice import Choice

from .tune_state import TuneState

import pandas as pd
import numpy as np

class TuneMaker(EpochManager, MemberManager):
    """
    Maker that creates the tuning model
    """

    def prepare_epoch(self, epoch):

        tuning_state = TuneState.get(epoch)
        if not tuning_state.get_tuning():
            return None

        prior_epoch = epoch.get_prior_epoch()
        prototype_member = prior_epoch.get_ranking().get_top_member()
        choices = prototype_member.get_choices()

        # Kill all members who don't share the top members choices!
        outside_members = [ m for m in epoch.list_members(alive = True) if m.get_choices() != choices ]
        for member in outside_members:
            member.kill("outside tune")

        tuning_state.set_prototype(prototype_member)

    def configure_mutation(self, member, prototype):
        member.impersonate(prototype)
        specialized, reason = member.specialize()
        return (specialized, reason)

    def configure_member(self, member):
        specie = member.get_specie() 
        epoch = specie.get_current_epoch() 
        tuning_state = TuneState.get(epoch)
        if not tuning_state.get_tuning():
            return (None, None)

        return self.configure_mutation(member, tuning_state.get_prototype())
