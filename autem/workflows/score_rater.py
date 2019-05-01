from ..member_manager import MemberManager
from ..scorers import MemberScoreState

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

        score_state = MemberScoreState.get(member)

        member.rated(score_state.score, score_state.score_std)
