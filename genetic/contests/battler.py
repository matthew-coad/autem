from ..simulators import Component

class Battler(Component):

    def contest_members(self, contestant1, contestant2, outcome):
        raise NotImplementedError("contest_members not implemented")
