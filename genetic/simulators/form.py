

class Form:

    def __init__(self, member):
        self.configuration = member.configuration
        self.count = 0

    def get_key(self):
        return repr(self.configuration)

