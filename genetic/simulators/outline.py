from enum import Enum
import os

class Role(Enum):
    ID = "ID",   # A resource identifer
    Property = "property",  # An input property of a resource
    Dimension = "dimension", # An input property that form an interesting dimension of a resource
    Measure = "measure", # A measure of an aspect of a resource
    KPI = "kpi", # An important measure of an aspect of a resource

class Attribute:

    def __init__(self, dataset, name, label, roles):
        self.name = name
        self.label = label
        self.roles = roles

class Outline:

    def __init__(self):
        self.attributes = []

