from .feedback import Feedback

class NullFeedback(Feedback):
    """
    Feedback object that ignores all feedback
    """

    def report(value, *args):
        """
        Feedback report
        """
        pass
