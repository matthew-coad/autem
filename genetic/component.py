from .dataset import Dataset
from .role import Role

from types import SimpleNamespace

class Component:

    def is_hyper_parameter(self):
        """
        Is this component a hyper parameter for the simulation
        """
        raise NotImplementedError()

    def is_controller(self):
        """
        Is this component responsible for controlling the simulation
        """
        raise NotImplementedError()

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        pass

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        pass
