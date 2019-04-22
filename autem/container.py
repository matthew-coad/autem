from types import SimpleNamespace

class Container:
    """
    Base class for the simulations state containers. Inherited by objects like simulation, specie and member.
    Contains base methods used by components to navigate the model, hold custom state etc.
    """

    def __init__(self):
        self._states = {}

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

    def list_components(self):
        return self.get_settings().get_components()

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
    def get_state(self, name, default = lambda: None):
        if not name in self._states:
            self._states[name] = default()
        return self._states[name]

    def set_state(self, name, value):
        self._states[name] = value

    def reset_state(self):
        self._states = {}
