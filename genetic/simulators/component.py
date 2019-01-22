
class Component:

    def start_simulation(self, simulation):
        """
        Start a simulation
        """
        pass

    def start_member(self, member):
        """
        Start a member
        """
        pass

    def evaluate_member(self, member, evaluation):
        """
        Perform a round of member evaluation
        """
        pass

    def battle_members(self, member1, member2, result):
        """
        Run a battle between two members
        """
        pass

    def outline_member(self, member, outline):
        """
        Outline what information is going to be supplied on a member
        """
        pass

    def record_member(self, member, report):
        """
        Record the state of a member
        """
        pass

    def report_simulation(self, simulation):
        """
        Report on the progress of a simulation
        """
        pass

