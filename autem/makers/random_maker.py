from .. import Maker, Member

class RandomMaker(Maker):

    """
    Maker that just builds members randomly
    """
    def make_member(self, specie):
        member = Member(specie)
        for component in specie.get_hyper_parameters():
            component.initialize_member(member)
        specialized = specie.specialize_member(member)
        if not specialized:
            member = None
        return member
