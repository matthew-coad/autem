from .attribute import Attribute

class Outline:

    def __init__(self):
        self.attributes = []

    def append_attribute(self, name, dataset, roles, label = None):
        if len(roles) == 0:
            raise RuntimeError("At least one role required")
        attribute = Attribute(name, dataset, roles, label = label)
        self.attributes.append(attribute)
        return attribute

    def has_attribute(self, name, dataset):
        """
        Does the outline contain the given attribute
        """
        exists = (name, dataset) in [(a.name, a.dataset) for a in self.attributes ]
        return exists
