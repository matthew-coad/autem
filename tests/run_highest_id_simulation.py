if __name__ == '__main__':
    import context

from tests.config import simulations_path

import autem
import autem.reporters as reporters

class configure_id(autem.HyperParameter):

    def __init__(self):
        self.name = "configure_id"

    def initialize_member(self, member):
        member.configuration.id = member.id

class highest_id_wins(autem.Controller):

    def contest_members(self, contestant1, contestant2, result):
        if contestant1.id > contestant2.id:
            result.decisive(1)
        else:
            result.decisive(2)

def run_highest_id_wins():
    path = simulations_path().joinpath("highest_id_wins")
    simulation = autem.Simulation("highest_id_wins", [configure_id(), highest_id_wins(), reporters.Path(path)], population_size=2)
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
