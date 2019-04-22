class StateContainer:
    """
    MixIn that adds the ability to add custom state to a container
    """

    # Evaluations
    def __init__(self):
        self.states = {}

    def get_states(self):
        return self._states

    def get_state(self, name, default = lambda: None):
        if not hasattr(self._states, name):
            setattr(self.evaluation, name, default())
        return getattr(self.evaluation, name)

    def set_evaluation(self, name, value):
        setattr(self.evaluation, name, value)


