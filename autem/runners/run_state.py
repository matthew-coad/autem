from .null_feedback import NullFeedback

class RunState:
    """
    State object responsible for tracking run time state of the simulation
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.feedback = NullFeedback()
        self.escaped = False

    def get(container):
        return container.get_state("run", lambda: RunState())
