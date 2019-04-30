class MasteryState:

    def __init__(self):
        self._current_choice_name = None
        self._current_component_name = None

    def get_current_choice_name(self):
        return self._current_choice_name

    def get_current_component_name(self):
        return self._current_component_name

    def set_current(self, choice_name, component_name):
        self._current_choice_name = choice_name
        self._current_component_name = component_name

    def get(container):
        return container.get_state("Master", lambda: MasteryState())

