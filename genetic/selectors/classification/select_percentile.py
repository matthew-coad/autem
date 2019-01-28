from ..selector import Selector
from ...simulators import Dataset, Role, ChoicesParameter

from sklearn.feature_selection import SelectPercentile as sk_SelectPercentile

class SelectPercentile(Selector):

    def __init__(self):
        Selector.__init__(self, "select_percentile", parameters=[
            ChoicesParameter("scorer", [ Role.Dimension ], "Select score", ["none", "f_classif", "mutual_info_classif", "chi2" ], "none" ),
            ChoicesParameter("percentage", [ Role.Dimension ], "Select percent", [10, 20, 50, 90, 100], 10),
        ])

