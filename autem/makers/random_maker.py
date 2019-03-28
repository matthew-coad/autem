from .. import Maker, Member

class RandomMaker(Maker):

    """
    Maker that just builds members randomly
    """
    def make_member(self, simulation):
        member = Member(simulation)
        for component in simulation.hyper_parameters:
            component.initialize_member(member)
        return member
