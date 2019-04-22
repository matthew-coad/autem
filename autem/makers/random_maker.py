from .maker import Maker

class RandomMaker(Maker):

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        if not member.get_specie().is_spotchecking():
            return False
            
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        return True
