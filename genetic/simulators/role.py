from enum import Enum

class Role(Enum):
    ID = "ID"   # A resource identifer
    Property = "property"  # An input property of a resource
    Dimension = "dimension" # An input property that form an interesting dimension of a resource
    Measure = "measure" # A measure of an aspect of a resource
    KPI = "kpi" # An important measure of an aspect of a resource
