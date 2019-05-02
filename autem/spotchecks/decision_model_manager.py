from ..epoch_manager import EpochManager
from ..member_manager import MemberManager

from ..scorers import MemberLeagueState
from ..scorers import MemberScoreState
from ..component_state import ComponentState
from .decision_model_state import DecisionModelState

import numpy as np
import pandas as pd

class DecisionModelManager(EpochManager, MemberManager):

    """
    Base class for decision model managers.

    Decision model managers are responsible for the creation of decision models. 
    Decision models  are used by member builders to decide on which members to introduce to the simulation.
    """

    def __init__(self):
        EpochManager.__init__(self)
        MemberManager.__init__(self)

    def build_decisions_df(self, simulation):
        """
        Build a dataframe of all decisions made during a simulation
        """

        # Collect all members including ones from the graveyard and from previous species 
        # for which we have reasonable accurate scores
        all_members = [ m for s in simulation.list_species() for m in s.list_members(buried = True) if MemberLeagueState.get(m).is_pro() ]
        if not all_members:
            return None

        # Build a frame containing for each member the decisions related to each choice
        choices = ComponentState.get(simulation).list_choices()
        member_decisions = {
            "member_id": [ m.id for m in all_members ]
        }
        get_decisions = lambda choice: [ choice.get_active_component_name(m) for m in all_members ]
        for choice in choices:
            member_decisions[choice.get_name()] = get_decisions(choice)
        decision_df = pd.DataFrame(member_decisions)

        # Build a frame containing fit score for each member
        scores = [(m.id, MemberScoreState.get(m).get_score()) for m in all_members ]
        score_df = pd.DataFrame(scores, columns=['member_id', 'score'])

        # Join the frames together
        decision_score_df = pd.merge(decision_df, score_df, on='member_id', how='inner')

        # Determine max score per component group
        choice_names = [ c.get_name() for c in choices ]
        decision_score_df = decision_score_df.groupby(choice_names, as_index=False).agg({"score": "max"})
        return decision_score_df

    def build_model(self, simulation):
        """
        Required override that builds the decision model
        """
        raise NotImplementedError()

    def evaluate_model(self, specie):

        # Build the model
        decisions_df = self.build_decisions_df(specie.get_simulation())
        model = self.build_model(specie.get_simulation(), decisions_df) if not decisions_df is None else None
        DecisionModelState.get(specie).set_decision_model(model)

        # Reset the expected score for all members
        #for member in specie.list_members():
        #    member.set_state("choice", ChoiceState())

    def prepare_epoch(self, epoch):
        self.evaluate_model(epoch.get_specie())

    def build_predicted_score(self, member):
        """
        Evaluate the expected score for a member
        """

        # Get the model
        specie = member.get_specie()
        model = specie.get_state("component_score_model")
        if model is None:
            return (None, None)

        # Build the choices into a dataframe
        choices = [ c for c in specie.list_hyper_parameters() if isinstance(c, Choice) ]
        choice_values = dict([ (c.get_name(), [c.get_active_component_name(member)]) for c in choices])
        x = pd.DataFrame(choice_values)

        # And do the prediction
        pred_y, pred_y_std = model.predict(x, return_std=True)
        return (pred_y[0], pred_y_std[0])

    #def evaluate_member(self, member):

    #    choice_state = get_choice_state(member)
    #    if not choice_state.choice_predicted_score is None:
    #        return None

    #    choice_predicted_score, choice_predicted_score_std = self.build_predicted_score(member)
    #    choice_state.choice_predicted_score = choice_predicted_score
    #    choice_state.choice_predicted_score_std = choice_predicted_score_std

    #def record_member(self, member, record):
    #    super().record_member(member, record)

    #    choice_state = get_choice_state(member)
    #    record.CE_score = choice_state.choice_predicted_score
    #    record.CE_score_std = choice_state.choice_predicted_score_std


