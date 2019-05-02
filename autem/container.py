from types import SimpleNamespace
from .setting_state import SettingState
from .component_state import ComponentState

class Container:
    """
    Base class for the simulations state containers. Inherited by objects like simulation, specie and member.
    Contains base methods used by components to navigate the model, hold custom state etc.
    """

    def __init__(self):
        self._setting_state = SettingState(self)
        self._component_state = ComponentState(self)
        self._states = {}

    # Context

    def get_simulation(self):
        """
        Required override that fetches the root simulation
        """
        raise NotImplementedError()

    def get_parent(self):
        """
        Required override that fetches the parent container
        """
        raise NotImplementedError()

    # States

    def settings(self):
        """
        Get the containers settings state
        """
        return self._setting_state

    def components(self):
        """
        Get the containers components state
        """
        return self._component_state

    def list_components(self):
        return self.get_simulation().list_components()

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

    # Settings

