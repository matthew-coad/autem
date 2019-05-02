from .container import Container

class SettingState:

    def __init__(self, container):

        assert isinstance(container, Container)

        self._container = container
        self._setting_data = {}

    def get_container(self):
        """
        Get the container the settings relate to
        """
        return self._container

    def set(key, value):
        """
        Assign a settings value
        """
        self._setting_data[key] = value

    def get(key, default = lambda: None):
        if key in self._setting_data:
            return self._setting_data[key]

        parent = self.get_container().get_parent()
        if parent is None:
            return default()
        return parent.set_settings().get(key, default)
