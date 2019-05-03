class DecisionState:

    def __init__(self, decision):
        assert isinstance(decision, tuple)
        self._decision = decision
        self._priority = 0
        self._introductions = 0

    def get_decision(self):
        return self._decision

    def get_priority(self):
        return self._priority

    def get_introductions(self):
        return self._introductions

    def prioritise(self, priority):
        self._priority = priority

    def introduce(self):
        self._introductions += 1

