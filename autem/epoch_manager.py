class EpochManager:

    ## Epoch components

    def configure_epoch(self, epoch):
        """
        Configure the epoch
        Value is the first component that returns a Non-Null value
        """
        pass

    def prepare_epoch(self, epoch):
        """
        Notification that an epoch is being started
        """
        pass

    def is_epoch_finished(self, epoch):
        """
        Is the epoch finished.
        """
        return (None, None)

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

    def bury_epoch(self, epoch):
        """
        Notification that an epoch is being finished
        """
        pass


class EpochManagerContainer:

    def list_epoch_managers(self):
        managers = [c for c in self.list_components() if isinstance(c, EpochManager) ]
        return managers
