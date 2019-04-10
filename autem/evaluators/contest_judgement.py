class ContestJudgement:

    def __init__(self):
        self.contests = None
        self.victories = None
        self.meaningful = None
        self.outcome = None
        

def get_contest_judgement(member):
    """
    Get contest judgement for an evaluation
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "contest_judgement"):
        evaluation.contest_judgement = ContestJudgement()
    return evaluation.contest_judgement
