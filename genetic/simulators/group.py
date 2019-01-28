from types import SimpleNamespace

class Group(SimpleNamespace):

    def __init__(self):
        self.components = []
        self.active = None
