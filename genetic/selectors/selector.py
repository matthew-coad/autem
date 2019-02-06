from ..simulators import Component

class Selector(Component):

    def __init__(self, name, label, parameters):
        Component.__init__(self, name, "selector", parameters)
        self.label = label

    pass
