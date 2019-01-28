from .loader import Loader

class Data(Loader):
    
    def __init__(self, x, y):
        Loader.__init__(self, "Data")
        self.x = x
        self.y = y

    def load_divided(self):
        return (self.x, self.y)
