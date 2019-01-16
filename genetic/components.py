
class Component:

    # Member overrides

    def initializeMember(self, member):
        """
        Initialize configuration for a new member of a population
        """
        pass

    def copyMember(self, member, parent0):
        """
        Initialize configuration for a member as a copy of a member from
        a previous population
        """
        pass

    def crossoverMember(self, member, parent0, parent1):
        """
        Initialize configuration for a new member as a crossover of the parents with
        parent0 being the "preferred" parent.
        IE copy parent0's state unless you want to "mix-it-up" deeper
        """
        pass

    def evaluateMember(self, member):
        """
        Update the evaluation state for a member of a population
        """
        pass

    def reportMember(self, member, row):
        """
        Report on the final state of the member
        """
        pass

    # Population overrides

    def initializePopulation(self, population):
        """
        Initialize configuration for a new population
        """
        pass

    def evaluatePopulation(self, population):
        """
        Evaluate state for a population
        """
        pass

    def competePopulation(self, population):
        """
        Perform population competition
        """
        pass

    def breedPopulation(self, population):
        """
        Perform population breeding
        """
        pass

    def reportPopulation(self, member, row):
        """
        Report on the population
        """
        pass

    def savePopulation(self, population):
        """
        Save population 
        """
        pass

    # Battle methods

    def battleMembers(self, population, member1, member2):
        """
        Run a battle between two members.
        Returns the member postfix of the victor, 0 if the contest is a draw.
        """
        return 0

