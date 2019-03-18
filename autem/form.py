class Form:

    def __init__(self, id, key):
        self.id = id
        self.key = key
        self.reincarnations = 0
        self.incarnations = 0

    def incarnate(self):
        self.reincarnations += 1
        self.incarnations += 1

    def disembody(self):
        self.incarnations -= 1
