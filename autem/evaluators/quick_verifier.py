from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

import time
import warnings

class QuickVerifier(Evaluater):
    """
    Quick check that verifies if the score is anywhere near the ball-park.
    Does a single fit and the score is not within two-standard deviations of the top league then eliminate it
    """

    def __init__(self, max_sd = 2.5):
        """
        Maximum standard deviations the evaluation must be within
        """
        self.max_sd = max_sd

    def evaluate_member(self, member):
        super().evaluate_member(member)

        evaluation = member.evaluation
        if hasattr(evaluation, "verification"):
            return None

        evaluation.verification = "failed"
        simulation = member.simulation
        resources = member.resources
        random_state = simulation.random_state

        scorer = simulation.resources.scorer
        loader = simulation.resources.loader

        x,y = loader.load_training_data(simulation)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=random_state)

        start = time.time()
        pipeline = resources.pipeline

        with WarningInterceptor() as messages:
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    pipeline.fit(x_train, y_train)
                    y_pred = pipeline.predict(x_test)
                except Warning as ex:
                    raise ex
            if messages:
                raise messages[0]

        end = time.time()
        duration = end - start
        score = scorer.score(y_test, y_pred)
        evaluation.verification_score = score
        evaluation.verification_duration = duration

        candidates = [ m for m in simulation.members if m.id != member.id and hasattr(m.evaluation, "score") and m.league > 0 and hasattr(m.evaluation, "verification_duration") ]
        if not candidates:
            evaluation.verification = "early"
            return None

        verification_scores = []
        verification_durations = []
        for candidate in candidates:
            verification_scores = verification_scores + candidate.evaluation.scores
            verification_durations.append(candidate.evaluation.verification_duration)

        verification_score = np.mean(verification_scores)
        verification_score_sd = np.std(verification_scores)
        max_sd = self.max_sd
        minimum_score = verification_score - verification_score_sd * max_sd

        if score < minimum_score:
            # We are out of the score ball-park
            evaluation.verification = "%s<%s low score" % (score, minimum_score)
            member.fail(evaluation.verification, "verify", "quick_verify")
            return None

        verification_duration = np.mean(verification_durations)
        verification_duration_sd = np.std(verification_duration)
        max_duration_sd = self.max_sd
        minimum_duration = verification_duration - verification_duration_sd * max_sd

        if duration > verification_duration * 5:
            # We are more than 5 times the mean duration
            evaluation.verification = "%s>%s 5xduration" % (duration, verification_duration * 5)
            member.fail(evaluation.verification, "verify", "quick_verify")
            return None

        evaluation.verification = "verified"

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "verification"):
            record.verification = evaluation.verification
        else:
            record.verification = None
