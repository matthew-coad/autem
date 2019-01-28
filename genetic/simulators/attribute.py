class Attribute:

    def __init__(self, name, dataset, roles, label = None):
        self.name = name
        self.dataset = dataset
        self.roles = roles
        if not label is None:
            self.label = label
        else:
            self.label = name
