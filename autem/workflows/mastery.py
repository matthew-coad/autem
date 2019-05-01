from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager

from ..scorers import MemberScoreManager, MemberScoreState
from .choice_evaluator import ChoiceEvaluator
from .duration_evaluator import DurationEvaluator

from .score_contest import ScoreContest
from .diverse_contest import DiverseContest

from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from .cross_over_maker import CrossoverMaker
from .top_choice_maker import TopChoiceMaker
from .random_maker import RandomMaker
from .tune_maker import TuneMaker
from .tune_state import TuneState
from .mastery_state import MasteryState

from ..choice import Choice

import time

class Mastery(SimulationManager, SpecieManager, EpochManager):
    """
    The mastery process analyses each pipeline choice and selects the best before moving onto the next choice.
    """

    def __init__(self, mastery_choices, max_time = None, max_epochs = None) :
        self._mastery_choices = mastery_choices
        self._max_time = max_time
        self._max_epochs = max_epochs

    def get_max_time(self):
        return self._max_time

    def get_max_rounds(self):
        return 20

    def get_max_league(self):
        return 4

    def get_max_population(self):
        return 20

    def get_max_reincarnations(self):
        return 3

    def get_max_epochs(self):
        return self._max_epochs

    def get_mastery_choices(self):
        return self._mastery_choices

    # Simulations

    def list_snapshot_extensions(self):
        extensions = [
            ScoreEvaluator(),
            ChoiceEvaluator(),
            DurationEvaluator(),

            ScoreContest(),
            DiverseContest(1.0),

            RandomMaker(),
            CrossoverMaker(),

            ContestJudge(),
           
            ScoreRater(),
        ]
        return extensions


    def configure_simulation(self, simulation):
        """
        Configure the simulation
        """
        components = simulation.list_components()
        snapshot_index = components.index(self)
        components[snapshot_index+1:snapshot_index+1] = self.list_snapshot_extensions()
        simulation.set_components(components)

    def is_simulation_finished(self, simulation):
        """
        Simulation is finished if all mastery choices are complete
        """
        duration = time.time() - simulation.get_start_time()
        choice_name, component_name = self.get_next_specie_configuration(simulation)

        if choice_name is None:
            return (True, "All choices processed")

        max_time = self.get_max_time()
        if max_time is not None and duration >= max_time:
            return (True, "Reached max time")
        
        return (False, None)

    # Species

    def get_next_specie_configuration(self, simulation):
        mastery_choices = self.get_mastery_choices()
        mastery_state = MasteryState.get(simulation)

        mastery_choice = mastery_choices[0]

        choices = [ c for c in simulation.list_components() if isinstance(c, Choice) ]
        choice_names = [ c.get_name() for c in choices ]
        choice_index = choice_names.index(mastery_choice)
        choice = choices[choice_index]
        choice_name = choice.get_name()

        component_names = choice.get_component_names()
        current_component_name = mastery_state.get_current_component_name()
        if current_component_name is None:
            component_name = component_names[0]
        else:
            current_index = component_names.index(current_component_name)
            component_index = current_index + 1
            if component_index >= len(component_names):
                choice_name = None
                component_name = None
            else:
                component_name = component_names[component_index]

        return (choice_name, component_name)

    def configure_specie(self, specie):
        simulation = specie.get_simulation()
        mastery_state = MasteryState.get(simulation)

        specie.set_max_league(self.get_max_league())
        specie.set_max_reincarnations(self.get_max_reincarnations())
        specie.set_max_population(self.get_max_population())

        choice_name, component_name = self.get_next_specie_configuration(specie.get_simulation())
        specie.get_component_override().set_component_choices(choice_name, [ component_name ])
        mastery_state.set_current(choice_name, component_name)
        specie_name = "%s=%s" % (choice_name, component_name)
        specie.set_name(specie_name)

    def is_choice_finished(self, specie):
        """
        Is the current mastery choice finished?
        """
        mastery_state = MasteryState.get(simulation)

        current_choice_name = mastery_state.get_current_choice_name()
        choices = [ c for c in simulation.list_components() if isinstance(c, Choice) ]
        choice_names = [ c.get_name() for c in choices ]
        choice_index = choice_names.index(current_choice_name)
        choice = choices[choice_index]

        component_names = choice.get_component_names()
        current_component_name = mastery_state.get_current_component_name()
        current_index = component_names.index(current_component_name)
        return current_index == len(component_names)-1

    def is_specie_finished(self, specie):
        """
        Species are finished if:
        + we have exceeded max epochs
        + exceeded max duration
        + Or the specie is no longer progressing
        """
        epoch = specie.get_current_epoch()
        is_tuning = TuneState.get(epoch).get_tuning()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if not max_epochs is None and n_epochs >= max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")

        progressed, reason = self.has_epoch_progressed(epoch)
        if progressed == False and is_tuning:
            return (True, reason)

        return (False, None)

    # Epoch

    def has_epoch_progressed(self, epoch):

        prior_epoch = epoch.get_prior_epoch()
        if not prior_epoch:
            return (None, "First epoch")

        prior_top_member = prior_epoch.get_ranking().get_top_member()
        top_member = epoch.get_ranking().get_top_member()

        if not prior_top_member:
            return (None, "No prior top member")

        if not top_member:
            return (None, "No top member")

        prior_top_score_evaluation = MemberScoreState.get(prior_top_member)
        top_score_evaluation = MemberScoreState.get(top_member)

        score_progressed = top_score_evaluation.score > prior_top_score_evaluation.score
        if score_progressed:
            return (True, "Score improved")

        return (False, "No score progress")

    def configure_epoch(self, epoch):
        prior_epoch = epoch.get_prior_epoch()
        progressed, reason = self.has_epoch_progressed(prior_epoch) if prior_epoch else (None, None)

        prior_is_tuning = TuneState.get(prior_epoch).get_tuning() if prior_epoch else None
        tuning = (prior_epoch and prior_is_tuning) or progressed == False
        epoch.set_max_rounds(self.get_max_rounds())
        TuneState.get(epoch).set_tuning(tuning)

    def is_epoch_finished(self, epoch):
        return (False, None)
