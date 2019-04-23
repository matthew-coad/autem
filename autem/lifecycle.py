class LifecycleManager:

    ## Member components

    def prepare_member(self, member):
        """
        Notification that a member is being prepared
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

    def fail_member(self, member, fault, operation, component):
        """
        Notification that a member has failed
        """
        pass

    def kill_member(self, member):
        """
        Notification that a member is being killed
        """
        pass

    def finish_member(self, member):
        """
        Notification that a member is finished
        """
        pass

    def bury_member(self, member):
        """
        Notification that a member is being buried
        """
        pass

    ## Epoch components

    def start_epoch(self, epoch):
        """
        Notification that an epoch is being started
        """
        pass

    def judge_epoch(self, epoch):
        """
        Judge the current epoch
        """
        pass

    def finish_epoch(self, epoch):
        """
        Notification that an epoch is being finished
        """
        pass

    ## Specie components

    def start_specie(self, specie):
        """
        Start a specie
        """
        pass

    def judge_specie(self, specie):
        """
        Judge the specie
        """
        pass

    def finish_specie(self, specie):
        """
        Finish an speciee
        """
        pass

class LifecycleContainer:

    def list_lifecycle_managers(self):
        managers = [c for c in self.list_components() if isinstance(c, LifecycleManager) ]
        return managers
