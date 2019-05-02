class DecisionState:

    def __init__(self, decision):
        self._decision = decision
        self._priority = 0

    def get_decision(self):
        return self._decision

    def get_priority(self):
        return self._priority

    def prioritise(self, priority):
        self._priority = priority

