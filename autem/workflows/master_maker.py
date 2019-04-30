from ..member_manager import MemberManager

class MasteryMaker(MemberManager):

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        specie = member.get_specie()
            
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        specialized, reason = member.specialize()
        return (specialized, reason)
