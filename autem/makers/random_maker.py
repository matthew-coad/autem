from .. import Maker, Member

class RandomMaker(Maker):

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        for component in member.get_settings().get_hyper_parameters():
            component.initialize_member(member)
        return True
