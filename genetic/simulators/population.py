from .component import Component
from .member import Member


class Population:

    def __init__(self, simulation):
        self.id = simulation.generate_id()
        self.simulation = simulation
        self.members = []

    def make_member(self):
        """
        Make a new member
        """
        member = Member(self.simulation)
        self.members.append(member)
        return member


