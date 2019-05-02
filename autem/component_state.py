class ComponentState:

    def __init__(self, container):
        self._container = container

    def get_container(self):
        """
        Get the container the components relate to
        """
        return self._container

    def get_components(self):
        """
        Get the components
        """
        return self.get_container().get_simulation()._components
