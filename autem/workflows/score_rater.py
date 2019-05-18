from ..member_manager import MemberManager
from ..scorers import MemberScoreQuery

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score
import warnings

class ScoreRater(MemberManager):
    """
    Uses the score to rate a model
    """

    def rate_member(self, member):
        """
        Evaluate the rating for a member.
        Only famous members get a rating.
        """

        scores = MemberScoreQuery(member)

        member.rated(scores.get_score(), scores.get_score_std())
