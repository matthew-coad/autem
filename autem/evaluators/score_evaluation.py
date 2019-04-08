class ScoreEvaluation:

    def __init__(self):
        self.quick_score = None
        self.quick_duration = None

        self.league_scores = {}
        self.league_durations = {}
        self.league_predictions = {}

        self.scores = []
        self.score = None
        self.score_std = None

        self.score_durations = []
        self.score_duration = None
        self.score_duration_std = None

def get_score_evaluation(member):
    """
     Get score evaluation for a member
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "score_evaluation"):
        evaluation.score_evaluation = ScoreEvaluation()
    return evaluation.score_evaluation

