from enum import Enum

class Role(Enum):
    ID = "ID"   # A resource identifer
    Parameter = "Paramter" # A hyper parameter of the simulation
    Property = "property"  # An input property of a resource
    Configuration = "configuration" # Property that defines the configuration
    Measure = "measure" # A measure of an aspect of a resource
    KPI = "kpi" # An important measure of an aspect of a resource
