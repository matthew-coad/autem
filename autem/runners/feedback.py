class Feedback:
    """
    Base for objects used to provide feedback to the user on the
    progess of the simulations.
    """

    def __init__(self):
        pass

    def report(self, *args):
        """
        Feedback report
        """
        raise NotImplementedError()

    def section(self, name):
        """
        Report on the start of a new section
        """
        self.report("----------- %s -----------" % name)

    def progress(self, iteration, total, prefix = '', suffix = ''):
        """
        Report progress
        """
        raise NotImplementedError()

