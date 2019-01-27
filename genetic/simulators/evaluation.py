
from types import SimpleNamespace

class Evaluation(SimpleNamespace):

    # Member evaluation result

    def __init__(self, member_id):
        self.member_id = member_id
        self.errors = 0
        self.exception = None

    def failed(self, ex):
        self.errors += 1
        self.exception = ex

