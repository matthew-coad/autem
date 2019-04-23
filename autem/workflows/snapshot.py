from .workflow import Workflow

from ..evaluators import ScoreEvaluator, ChoiceEvaluator, ValidationEvaluator, DurationEvaluator
from ..evaluators import ScoreContest, DiverseContest
from ..evaluators import ContestJudge, EpochProgressJudge
from ..evaluators import ScoreRater
from ..makers import TopChoiceMaker, CrossoverMaker, TuneMaker

import time

class Snapshot(Workflow):
    """
    The snapshow workflow produces a very quick snapshot simulation that runs one specie with no tuning
    """

    def __init__(self, max_epochs = 2, max_time = None) :
        Workflow.__init__(self, max_time = max_time)
        self._max_epochs = max_epochs

    def get_max_epochs(self):
        return self._max_epochs

    # Simulations

    def list_snapshot_extensions(self):
        extensions = [
            ScoreEvaluator(),
            ChoiceEvaluator(),
            ValidationEvaluator(),
            DurationEvaluator(),

            ScoreContest(),
            DiverseContest(1.0),

            TopChoiceMaker(),
            CrossoverMaker(),
            TuneMaker(),

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
        Is the simulation finished.
        Simulation is finished if any component elects to finish it
        """
        n_species = len(simulation.list_species())
        if n_species > 0:
            return (True, "Ran specie")
        return (False, None)

    # Species

    def configure_specie(self, specie):
        specie.set_max_league(self.get_max_league())
        specie.set_mode("spotcheck")
        specie.set_max_reincarnations(self.get_max_reincarnations())
        specie.set_max_population(self.get_max_population())

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        epoch = specie.get_current_epoch()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if n_epochs >= max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)
