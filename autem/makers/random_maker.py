from .. import Maker, Member

class RandomMaker(Maker):

    """
    Maker that just builds members randomly
    """
    def make_member(self, simulation):
        member = Member(simulation)
        for component in simulation.hyper_parameters:
            component.initialize_member(member)
        specialized = simulation.specialize_member(member)
        if not specialized:
            member = None
        return member
