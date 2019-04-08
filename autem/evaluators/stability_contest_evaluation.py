class StabilityContestEvaluation:
    
    def __init__(self):
        self.stability_contest = None

def get_stability_contest_evaluation(member):
    """
     Get score contest evaluation for a member
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "stability_contest_evaluation"):
        evaluation.stability_contest_evaluation = StabilityContestEvaluation()
    return evaluation.stability_contest_evaluation

