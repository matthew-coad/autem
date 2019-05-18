from ..epoch_manager import EpochManager
from ..member_manager import MemberManager
from ..reporters import Reporter

from ..scorers import MemberScoreQuery
from ..component_state import ComponentState
from .decision_model_state import DecisionModelState
from .member_decision_state import MemberDecisionState
from .decision_grid_state import DecisionGridState

import numpy as np
import pandas as pd

class DecisionModelManager(EpochManager, MemberManager, Reporter):

    """
    Base class for decision model managers.

    Decision model managers are responsible for the creation of decision models. 
    Decision models  are used by member builders to decide on which members to introduce to the simulation.
    """

    def __init__(self):
        EpochManager.__init__(self)
        MemberManager.__init__(self)
        Reporter.__init__(self)

    def list_authorative_members(self, simulation):
        """
        List members who are considered an "authority" on decision models
        """
        members = [ m for s in simulation.list_species() for m in s.list_members(buried = True) if MemberScoreQuery(m).get_score() ]
        return members

    def build_member_decision_df(self, specie, members):
        """
        Build a decision df for a list of members.
        """
        assert members

        # Build a frame containing for each member the decisions related to each choice
        choices = ComponentState.get(specie).list_choices()
        member_decisions = {
            "member_id": [ m.id for m in members ]
        }
        get_decisions = lambda choice: [ choice.get_active_component_name(m) for m in members ]
        for choice in choices:
            member_decisions[choice.get_name()] = get_decisions(choice)
        decision_df = pd.DataFrame(member_decisions)
        return decision_df

    def build_decision_grid_df(self, specie, decision_grid):

        choices = ComponentState.get(specie).list_choices()
        x_values = {}
        for index, choice in enumerate(choices):
            x_values[choice.get_name()] = [ i.get_decision()[index] for i in decision_grid ]
        decision_grid_df = pd.DataFrame(data = x_values)
        return decision_grid_df

    def build_member_decision_score_df(self, specie, members):
        """
        Build a decision score df for a list of members
        """

        assert members
        decision_df = self.build_member_decision_df(specie, members)

        # Build a frame containing fit score for each member
        scores = [(m.id, MemberScoreQuery(m).get_score()) for m in members ]
        score_df = pd.DataFrame(scores, columns=['member_id', 'score'])

        # Join the frames together
        decision_score_df = pd.merge(decision_df, score_df, on='member_id', how='inner')

        # Determine max score per component group
        choices = ComponentState.get(specie).list_choices()
        choice_names = [ c.get_name() for c in choices ]
        decision_score_df = decision_score_df.groupby(choice_names, as_index=False).agg({"score": "max"})
        return decision_score_df

    def build_model(self, specie, members):
        """
        Required override that builds the decision model
        """
        raise NotImplementedError()

    def evaluate_model(self, specie):
        # Build the model
        simulation = specie.get_simulation()
        members = self.list_authorative_members(simulation)
        model = self.build_model(specie, members) if members else None
        DecisionModelState.get(specie).evaluated(model)

    def evaluate_decision_priority(self, specie):
        """
        Evaluate the decision priorities for the decision grid
        """
        decision_model = DecisionModelState.get(specie).get_decision_model()
        decision_grid_state = DecisionGridState.get(specie)
        decision_grid = decision_grid_state.get_decision_grid()

        if decision_model is None or decision_grid is None or len(decision_grid) == 0:
            return

        decision_grid_df = self.build_decision_grid_df(specie, decision_grid)
        pred_y = decision_model.predict(decision_grid_df).tolist()

        for pred, decision in zip(pred_y, decision_grid):
            decision_grid_state.prioritise_decision(decision.get_decision(), pred)

    def prepare_epoch(self, epoch):
        specie = epoch.get_specie()
        self.evaluate_model(specie)
        self.evaluate_decision_priority(specie)

        # Reset the expected score for all members
        for member in specie.list_members():
            MemberDecisionState.get(member).reset()

    def evaluate_member(self, member):

        member_decision = MemberDecisionState.get(member)
        if member_decision.get_evaluated():
            return

        decision_grid_state = DecisionGridState.get(member.get_specie())
        if not decision_grid_state.get_prioritised():
            member_decision.evaluated(None)
            return

        decision_score = decision_grid_state.get_decision_priority(member.get_decision())
        member_decision.evaluated(decision_score)

    def record_member(self, member, record):
        super().record_member(member, record)

        member_decision = MemberDecisionState.get(member)
        record.CE_score = member_decision.get_decision_score()
