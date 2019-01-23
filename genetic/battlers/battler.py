from ..simulators import Component

class Battler(Component):

    def battle_members(self, contestant1, contestant2, result):
        raise NotImplementedError("Battle_members not implemented")
