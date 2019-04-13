class VotingEvaluation:

    def __init__(self):
        self.base_score = None
        self.combined_score = None
        self.score_boost = None
        self.evaluated = False
        self.victories = 0

def get_voting_evaluation(member):
    """
     Get voting evaluation for a member
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "voting_evaluation"):
        evaluation.voting_evaluation = VotingEvaluation()
    return evaluation.voting_evaluation

