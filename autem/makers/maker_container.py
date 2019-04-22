from .maker import Maker

class MakerContainer:

    def list_makers(self):
        makers = [c for c in self.list_components() if isinstance(c, Maker) ]
        return makers
