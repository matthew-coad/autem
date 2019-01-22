from enum import Enum
import os

class Dataset(Enum):
    Battle = "battle"

class Role(Enum):
    ID = "ID"   # A resource identifer
    Property = "property"  # An input property of a resource
    Dimension = "dimension" # An input property that form an interesting dimension of a resource
    Measure = "measure" # A measure of an aspect of a resource
    KPI = "kpi" # An important measure of an aspect of a resource

class Attribute:

    def __init__(self, name, dataset, roles, label = None):
        self.name = name
        self.dataset = dataset
        self.roles = roles
        if not label is None:
            self.label = label
        else:
            self.label = name

class Outline:

    def __init__(self):
        self.attributes = []

    def make_attribute(self, name, dataset, roles, label = None):
        attribute = Attribute(name, dataset, roles, label = label)
        self.attributes.append(attribute)
        return attribute

