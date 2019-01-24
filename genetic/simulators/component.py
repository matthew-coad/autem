
class Component:

    def start_simulation(self, simulation):
        """
        Start a simulation
        """
        pass

    def outline_simulation(self, simulation, outline):
        """
        Outline what information is going to be supplied by a simulation
        """
        pass

    def start_member(self, member):
        """
        Start a member
        """
        pass

    def copy_member(self, member, prior):
        """
        Start a member
        """
        pass

    def mutate_member(self, member, prior):
        """
        Mutate a member
        """
        return False

    def evaluate_member(self, member, evaluation):
        """
        Perform a round of member evaluation
        """
        pass

    def contest_members(self, member1, member2, outcome):
        """
        Run a battle between two members
        """
        pass

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        pass

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        pass

