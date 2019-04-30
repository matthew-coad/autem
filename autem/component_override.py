class ComponentOverride:

    def __init__(self, container):
        self._container = container
        self._component_enabled = {}
        self._component_choices = {}

    # Properties

    def get_container(self):
        return self._container

    def set_component_enabled(self, component_name, enabled):
        """
        Locally set the component enabled flag
        """
        self._component_enabled[component_name] = enabled

    def get_component_enabled(self, component_name):
        """
        Determine if the component is enabled by searching the override chain
        """
        if component_name in self._component_enabled:
            return self._component_enabled[component_name]
        parent = self.get_container().get_parent()
        if parent is None:
            return True
        return parent.get_component_override().get_component_enabled(component_name)

    def set_component_choices(self, component_name, choices):
        """
        Locally set the component enabled flag
        """
        self._component_choices[component_name] = choices

    def get_component_choices(self, component_name):
        if component_name in self._component_choices:
            return self._component_choices[component_name]
        parent = self.get_container().get_parent()
        if parent is None:
            return None
        return parent.get_component_override().get_component_choices(component_name)


class ComponentOverrideContainer:

    def __init__(self):
        self._component_override = ComponentOverride(self)

    def get_component_override(self):
        return self._component_override
