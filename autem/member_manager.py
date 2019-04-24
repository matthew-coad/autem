class MemberManager:

    ## Simulation managers

    def configure_member(self, simulation):
        """
        Configure a member
        """
        return (None, None)

    def prepare_member(self, simulation):
        """
        Prepare a member for evaluation
        """
        pass

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        pass

    def contest_members(self, member1, member2):
        """
        Run a contest between two members
        """
        pass

    def judge_member(self, member):
        """
        Determine the fate of a member
        """
        pass

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """
        pass

    def finish_member(self, member):
        """
        Finish up the simulation. Perform final reporting, collect stats, etc.
        """
        pass

    def bury_member(self, member):
        """
        Bury any expensive resources allocated to the member
        """
        pass

class MemberManagerContainer:

    def list_member_managers(self):
        managers = [c for c in self.list_components() if isinstance(c, MemberManager) ]
        return managers
