from types import SimpleNamespace

class Container:
    """
    Base class for the simulations state containers. Inherited by objects like simulation, specie and member.
    Contains base methods used by components to navigate the model, hold custom state etc.
    """

    def __init__(self):
        self._states = SimpleNamespace()

    # Context

    def get_simulation(self):
        """
        Required override that fetches the root simulation
        """
        pass

    # State
    def get_states(self):
        return self._states

    def get_state(self, name, default = lambda: None):
        if not hasattr(self._states, name):
            setattr(self._states, name, default())
        return getattr(self._states, name)

    def set_state(self, name, value):
        setattr(self._states, name, value)

