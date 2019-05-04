class SettingState:

    def __init__(self, container):
        self._container = container

    def set_value(self, key, value):
        """
        Assign a settings value
        """
        self._container._setting_data[key] = value

    def get_value(self, key, default = lambda: None):
        setting_data = self._container._setting_data
        if key in setting_data:
            return setting_data[key]

        parent = self._container.get_parent()
        if parent is None:
            return default()
        return SettingState.get(parent).get_value(key, default)

    def get(container):
        return SettingState(container)
