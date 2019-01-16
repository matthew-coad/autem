from .reportManager import ReportManager

from enum import Enum
import os

class AttributeRole(Enum):
    ID = "ID",   # A resource identifer
    Property = "property",  # An input property of a resource
    Dimension = "dimension", # An input property that form an interesting dimension of a resource
    Measure = "measure", # A measure of an aspect of a resource
    KPI = "kpi", # An important measure of an aspect of a resource
    Unknown = "unknown" # An unknown/unclassified attribute

class AttributeInfo:

    def __init__(self, name, label, role):
        self.name = name
        self.label = label
        self.role = role

class MetaInfo:

    def __init__(self, simulations, population_attributes, member_attributes):
        self.simulations = simulations
        self.population_attributes = population_attributes
        self.member_attributes = member_attributes

# Library of standard attributes        

type_role = {
    "id" : AttributeRole.ID,
    "property" : AttributeRole.Property,
    "prop" : AttributeRole.Property,
    "dim" : AttributeRole.Dimension,
    "dimension" : AttributeRole.Dimension,
    "measure" : AttributeRole.Measure,
    "kpi" : AttributeRole.KPI
}

class MetaManager:
    """
    Simulations meta information manager
    """

    def __init__(self, path):
        """
        Create a meta manager for a simulation
        """
        self.path = path

    def evaluate_attribute(self, column):
        """
        Evaluate an attribute
        """
        parts = column.split("_")

        if len(parts) > 1 and parts[-1] in type_role:
            role = type_role[parts[-1]]
        else:
            role = AttributeRole.Unknown

        if len(parts) > 1 and role != AttributeRole.Unknown:
            label = "_".join(parts[:-1])
        else:
            label = column

        attribute = AttributeInfo(column, label, role)
        return attribute

    def get_simulation_path(self, simulation):
        return self.path.joinpath(simulation)

    def get_simulation_info(self, simulation):
        """
        Get meta information for a simulation
        """
        report_manager = ReportManager(self.get_simulation_path(simulation))
        population_report = report_manager.read_population_report()
        member_report = report_manager.read_member_report()
        population_attributes = [self.evaluate_attribute(c) for c in population_report.columns]
        member_attributes = [self.evaluate_attribute(c) for c in member_report.columns]

        info = MetaInfo([simulation], population_attributes, member_attributes)
        return info

    def get_simulations(self):
        """
        List all available simulations
        """
        directories = [n for n in os.listdir(self.path) if os.path.isdir(self.path.joinpath(n))]
        return directories

    def get_meta_info(self):
        simulations = self.get_simulations()
        simulation_infos = [ self.get_simulation_info(s) for s in simulations]

        all_population_attributes = [ pop for si in simulation_infos for pop in si.population_attributes]
        all_member_attributes = [ ma for si in simulation_infos for ma in si.member_attributes]

        population_attributes = {}
        for pa in all_population_attributes:
            if not pa.name in population_attributes:
                population_attributes[pa.name] = pa

        member_attributes = {}
        for ma in all_member_attributes:
            if not ma.name in member_attributes:
                member_attributes[ma.name] = ma

        info = MetaInfo(simulations, list(population_attributes.values()), list(member_attributes.values()))
        return info
