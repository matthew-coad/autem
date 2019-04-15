class ScoreResources:

    def __init__(self):
        self.quick_predictions = None
        self.league_predictions = {}

def get_score_resources(member):
    """
     Get score resources for a member
    """
    return member.get_resource("score", lambda: ScoreResources())
