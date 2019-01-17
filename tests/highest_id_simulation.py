if __name__ == '__main__':
    import context

import genetic
from pathlib import Path

class IDRating(genetic.Component):

    def initializeMember(self, member):
        member.configuration.rating = member.id

    def copyMember(self, member, parent0):
        member.configuration.rating = parent0.configuration.rating

    def crossoverMember(self, member, parent0, parent1):
        member.configuration.rating = parent0.configuration.rating

    def reportMember(self, member, row):
        row.rating = member.configuration.rating

    def battleMembers(self, population, member1, member2):
        if member1.configuration.rating > member2.configuration.rating:
            return 1
        elif member1.configuration.rating < member2.configuration.rating:
            return 2
        else:
            return 0

def runHighestIDSimulation():

    name = "highest_id"
    path = Path("tests", "simulations", name)

    components = [
        genetic.FixedPopulationSize(20),
        IDRating(),
        genetic.BattleCompetition(5, 5, .5),
        genetic.SavePath(path)
    ]
    simulation = genetic.Simulation(name, components)
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()
    simulation.run()

if __name__ == '__main__':
    runHighestIDSimulation()
