from types import SimpleNamespace

class Container:
    """
    Base class for the model containers.
    """

    def __init__(self):
        self._states = {}

    # Context

    def get_parent(self):
        """
        Required override that fetches the parent container
        """
        raise NotImplementedError()

    # States

    def get_state(self, name, default = lambda: None):
        if not name in self._states:
            self._states[name] = default()
        return self._states[name]

    def set_state(self, name, value):
        self._states[name] = value

    def reset_state(self):
        self._states = {}


