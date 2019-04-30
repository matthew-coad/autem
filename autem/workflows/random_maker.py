from ..member_manager import MemberManager

class RandomMaker(MemberManager):

    name = "RandomMaker"

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
            
        specialized, reason = member.specialize()
        return (specialized, reason)
