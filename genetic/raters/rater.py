from ..simulators import Component

class Rater(Component):

    def rate_member(self, member, rating):
        raise NotImplementedError()
