if __name__ == '__main__':
    import context

from tests.config import simulations_path

import genetic.simulators as simulators
import genetic.reporters as reporters


class highest_id_wins(simulators.Component):

    def __init__(self):
        simulators.Component.__init__(self, "highest_id_wins")

    def start_member(self, member):
        member.configuration.id = member.id

    def contest_members(self, contestant1, contestant2, result):
        if contestant1.id > contestant2.id:
            result.decisive(1)
        else:
            result.decisive(2)

def run_highest_id_wins():
    simulation = simulators.Simulation("highest_id_wins", [highest_id_wins(), reporters.Path(simulations_path())], population_size=2)
    simulation.start()
    simulation.step()
    simulation.step()
    simulation.step()
    simulation.report()
    simulation.step()
    simulation.step()
    simulation.step()
    simulation.report()


if __name__ == '__main__':
    run_highest_id_wins()
