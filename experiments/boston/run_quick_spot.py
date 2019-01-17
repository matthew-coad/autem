# First tuning model

if __name__ == '__main__':
    import context

import tests.quick_spot_simulation as quick_spot

import genetic
import genetic.scorers as scorers
import genetic.learners as learners

from pathlib import Path
from pandas import read_csv

if __name__ == '__main__':
    simulation_name = "quick_spot"
    simulation = quick_spot.make_quick_spot_simulation(simulation_name, 100, Path("experiments", "boston", "simulations", simulation_name))
    quick_spot.run_quick_spot_simulation(simulation, 50)
