

class Parameter:

    def __init__(self, name, report_name = None):
        self.name = name
        self.report_name = report_name

    def initialValue(self, member):
        """
        Get the initial value of a member
        """
        raise NotImplementedError

    def generateValue(self, member):
        """
        Generate a new random value of a parameter
        """
        raise NotImplementedError

    def getMemberValue(self, learner, member):
        configuration = getattr(member.configuration.learners, learner.name)
        value = getattr(configuration, self.name)
        return value

    def setMemberValue(self, learner, member, value):
        configuration = getattr(member.configuration.learners, learner.name)
        setattr(configuration, self.name, value)

    def initializeParameter(self, learner, member):
        initial_value = self.initialValue(member)
        self.setMemberValue(learner, member, initial_value)

    def copyParameter(self, learner, member, parent0):
        value = self.getMemberValue(learner, parent0)
        self.setMemberValue(learner, member, value)

    def crossoverParameter(self, learner, member, parent0, parent1):
        random_state = member.simulation.random_state
        parent_index = random_state.randint(0, 2)
        if parent_index == 0:
            parent = parent0
        else:
            parent = parent1
        value = self.getMemberValue(learner, parent)
        self.setMemberValue(learner, member, value)

    def mutateParameter(self, learner, member):
        value = self.generateValue(member)
        self.setMemberValue(learner, member, value)

    def reportParameter(self, learner, member, row):
        if not self.report_name is None:
            value = self.getMemberValue(learner, member)
            setattr(row, self.report_name, value)

class ChoiceTuneParameter(Parameter):

    def __init__(self, name, report_name, choices):
        Parameter.__init__(self, name, report_name)
        self.choices = choices

    def initialValue(self, member):
        # Initial value is None.
        # Models have "good" default values which will be used in this case
        return None

    def generateValue(self, member):
        random_state = member.simulation.random_state
        choices = self.choices
        choice_index = random_state.randint(0, len(choices))
        choice = choices[choice_index]
        return choice
