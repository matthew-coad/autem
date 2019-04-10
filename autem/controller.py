from .component import Component
from types import SimpleNamespace

class Controller(Component):

    def is_hyper_parameter(self):
        """
        Is this component a hyper parameter for the simulation
        """
        return False

    def is_controller(self):
        """
        Is this component responsible for controlling the simulation
        """
        return True

    def start_simulation(self, simulation):
        """
        Start a simulation
        """
        pass

    def start_epoch(self, epoch):
        """
        Start a simulation epoch
        """
        pass

    def evaluate_member(self, member):
        """
        Perform a round of member evaluation
        """
        pass

    def contest_members(self, member1, member2):
        """
        Run a contest between two members
        """
        pass

    def judge_member(self, member):
        """
        Determine the fate of a member
        """
        pass

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """
        pass

    def judge_epoch(self, epoch):
        """
        Judge the current epoch
        """
        pass

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        pass

