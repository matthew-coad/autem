from .choice import Choice

class ComponentState:

    def __init__(self, container):
        self._container = container

    def get_container(self):
        """
        Get the container the components relate to
        """
        return self._container

    def list(self):
        """
        List all available components
        """
        return self.get_container().get_simulation()._components[:]

    def list_choices(self):
        """
        List all available choices
        """
        components = self.get_container().get_simulation()._components
        choices = [ c for c in components if isinstance(c, Choice) ]
        return choices

    def get(container):
        return ComponentState(container)
