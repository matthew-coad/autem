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
        List all possible choices
        """
        components = self.get_container().get_simulation()._components
        choices = [ c for c in components if isinstance(c, Choice) ]
        return choices

    def list_all_options(self, choice):
        """
        List all possible options for a choice.
        """
        assert isinstance(choice, Choice)
        return choice.components[:]

    def list_options(self, choice):
        """
        List options for a choice, taking into account choice constraints.
        """
        return self.list_all_options(choice)

    def get(container):
        """
        Get the choice state given a container
        """
        return ComponentState(container)
