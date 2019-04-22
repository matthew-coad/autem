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

    def get_settings(self):
        """
        Get shared settings object
        """
        return self.get_simulation().get_settings()

    def get_random_state(self):
        """
        Get shared random state object
        """
        return self.get_simulation().get_random_state()

    def generate_id(self):
        """
        Generate an ID unique to simulation
        """
        return self.get_simulation().generate_id()

    # State
    def get_states(self):
        return self._states

    def get_state(self, name, default = lambda: None):
        if not hasattr(self._states, name):
            setattr(self._states, name, default())
        return getattr(self._states, name)

    def set_state(self, name, value):
        setattr(self._states, name, value)

