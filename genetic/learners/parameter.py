

class Parameter:

    def __init__(self, name, report_name = None):
        self.name = name
        self.report_name = report_name

    def generateValue(self, member):
        """
        Generate an initial value of a parameter
        """
        raise NotImplementedError

    def getMemberValue(self, learner, member):
        configuration = getattr(member.configuration, learner.name)
        value = getattr(configuration, self.name)
        return value

    def setMemberValue(self, learner, member, value):
        configuration = getattr(member.configuration, learner.name)
        setattr(configuration, self.name, value)

    def initializeParameter(self, learner, member):
        initial_value = self.generateValue(member)
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

    def reportParameter(self, learner, member, row):
        if not self.report_name is None:
            value = self.getMemberValue(learner, member)
            setattr(row, self.report_name, value)

class ChoiceParameter(Parameter):

    def __init__(self, name, report_name, choices):
        Parameter.__init__(self, name, report_name)
        self.choices = choices

    def generateValue(self, member):
        random_state = member.simulation.random_state
        choices = self.choices
        choice_index = random_state.randint(0, len(choices))
        choice = choices[choice_index]
        return choice
