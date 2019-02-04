from ..selector import Selector
from ...simulators import Dataset, Role, ChoicesParameter

import sklearn.feature_selection as sk

class SelectPercentile(Selector):

    def __init__(self):
        Selector.__init__(self, "select_perc", parameters=[
            ChoicesParameter("scorer", [ Role.Configuration ], "Select scorer", ["none", "f_classif", "mutual_info_classif", "chi2" ], None),
            ChoicesParameter("percentile", [ Role.Configuration ], "Select percent", [10, 20, 50, 80, 90], None),
        ])

    def evaluate_member(self, member, evaluation):
        scorer = member.configuration.select_perc.scorer
        percentile = member.configuration.select_perc.percentile
        score_func = None
        if scorer == "f_classif":
            score_func = sk.f_classif
        elif scorer == "mutual_info_classif":
            score_func = sk.mutual_info_classif
        elif scorer == "chi2":
            score_func = sk.chi2

        if not score_func is None:
            if not hasattr(evaluation, "steps"):
                evaluation.steps = []
            selector = sk.SelectPercentile(score_func=score_func, percentile=percentile)
            evaluation.steps.append((self.name, selector))
