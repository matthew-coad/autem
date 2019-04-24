from ..member_manager import MemberManager


class RandomMaker(MemberManager):

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        if not member.get_specie().is_spotchecking():
            return (None, None)
            
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        specialized, reason = member.specialize()
        return (specialized, reason)
