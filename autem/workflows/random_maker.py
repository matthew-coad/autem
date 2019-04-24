from ..member_manager import MemberManager


class RandomMaker(MemberManager):

    """
    Maker that just builds members randomly
    """
    def configure_member(self, member):
        specie = member.get_specie()
        if specie.get_current_epoch().is_tuning():
            return (None, None)
            
        for component in member.list_hyper_parameters():
            component.initialize_member(member)
        specialized, reason = member.specialize()
        return (specialized, reason)
