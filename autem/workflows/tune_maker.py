from ..epoch_manager import EpochManager
from ..member_manager import MemberManager
from ..choice import Choice

import pandas as pd
import numpy as np

class TuneState():

    """
    Tune state
    """
    def __init__(self):
        self.choices = None
        self.prototype = None
        self.tuning = False

def get_tune_state(container):
    return container.get_state("tune", lambda: TuneState())

class TuneMaker(EpochManager, MemberManager):
    """
    Maker that creates the tuning model
    """

    def prepare_epoch(self, epoch):

        if not epoch.is_tuning():
            return None

        prior_epoch = epoch.get_prior_epoch()
        prototype_member = prior_epoch.get_ranking().get_top_member()
        choices = prototype_member.get_choices()

        # Kill all members who don't share the top members choices!
        outside_members = [ m for m in epoch.list_members(alive = True) if m.get_choices() != choices ]
        for member in outside_members:
            member.kill("outside tune")

        state = get_tune_state(epoch)
        state.choices = choices
        state.prototype = prototype_member
        state.tuning = True

    def configure_mutation(self, member, prototype):
        member.impersonate(prototype)
        specialized, reason = member.specialize()
        return (specialized, reason)

    def configure_member(self, member):
        specie = member.get_specie() 
        epoch = specie.get_current_epoch() 
        if not epoch.is_tuning():
            return (None, None)

        state = get_tune_state(epoch)
        return self.configure_mutation(member, state.prototype)
