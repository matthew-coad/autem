class Settings:

    """
    Base class for settings
    """

    def __init__(self, container):
        self._container = container

    def get_container(self):
        return self._container

    def set_value(self, key, value):
        """
        Assign a settings value
        """
        self.get_container()._states[key] = value

    def get_value(self, key, default = lambda: None):
        container = self.get_container()
        while not container is None:
            setting_data = container._states
            if key in setting_data:
                return setting_data[key]

            container = container.get_parent()
        return default()
