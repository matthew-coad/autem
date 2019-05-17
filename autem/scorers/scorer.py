from ..simulation_manager import SimulationManager
from ..member_manager import MemberManager
from ..specie_manager import SpecieManager
from ..reporters import Reporter

from .member_score_state import MemberScoreState
from .member_league_state import MemberLeagueState
from ..simulation_settings import SimulationSettings
from .score_settings import ScoreSettings
from .score_query import ScoreQuery

import numpy as np

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, RepeatedKFold

import warnings
import time

class Scorer(SimulationManager, MemberManager, SpecieManager, Reporter):

    def __init__(self, metric, n_splits):
        SimulationManager.__init__(self)
        MemberManager.__init__(self)
        SpecieManager.__init__(self)
        Reporter.__init__(self)
        self.metric = metric
        self.n_splits = n_splits

    # Simulation

    def prepare_simulation(self, simulation):
        """
        Make the score metric accessible across the application
        """
        ScoreSettings(simulation).set_metric(self.metric)

    # Specie

    def prepare_specie(self, specie):
        """
        Prepare folds
        """
        folds = self.build_folds(specie)
        ScoreSettings(specie).set_folds(folds)

    def build_folds(self, specie):
        """
        Build the folds for a given specie
        """
        max_league = SimulationSettings(specie).get_max_league()
        random_state = SimulationSettings(specie).get_random_state()

        data = specie.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        fold = RepeatedStratifiedKFold(n_splits=self.n_splits, n_repeats=max_league, random_state=random_state)
        folds = [ (i_train, i_test) for i_train, i_test in fold.split(x, y) ]
        return folds

    # Member

    def evaluate_member(self, member):

        score_state = MemberScoreState.get(member)
        if member.league == 0 and score_state.quick_score is None:
            self.evaluate_quick_score(member)
            return None

        # At league level 1 add on the complete scores
        evaluated = False
        if member.league == 1 and not 1 in score_state.league_scores:
            evaluated = self.evaluate_league_1(member)

        # High league levels
        if member.league > 1 and not member.league in score_state.league_scores:
            evaluated = self.evaluate_league_scores(member, member.league)

        if evaluated:
            self.evaluate_scores(member)

    def get_folds(self, specie, repeat, start, stop):
        start_index = self.n_splits * repeat + start
        end_index = self.n_splits * repeat + start + stop
        folds = ScoreSettings(specie).get_folds()[start_index:end_index]
        return folds

    def build_scores(self, member, folds):
        """
        Build scores for the given member for the given folds
        """

        metric = ScoreQuery(member).get_metric()
        pipeline = member.get_pipeline()

        data = member.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        scores = []
        durations = []
        predictions = np.empty(len(y))
        predictions[:] = np.nan
        for fold in folds:
            i_train = fold[0]
            i_test = fold[1]
            x_train = x[i_train]
            y_train = y[i_train]
            x_test = x[i_test]
            y_test = y[i_test]
            start_time = time.time()

            with warnings.catch_warnings():
                warnings.simplefilter("error")
                try:
                    pipeline.fit(x_train, y_train)
                    y_pred = pipeline.predict(x_test)
                except Exception as ex:
                    member.fail(ex, "score_evaluator", "ScoreEvaluator")
                    return (None, None, None)
            end_time = time.time()
            duration = end_time - start_time
            score = metric(y_test, y_pred)
            scores.append(score)
            durations.append(duration)
            predictions[i_test] = y_pred
        return (scores, durations, predictions)

    def evaluate_quick_score(self, member):
        """
        Evaluate a quick score based on a single fit using the first entry in quick_fold
        """
        folds = self.get_folds(member.get_specie(), 0, 0, 1)
        scores, durations, predictions = self.build_scores(member, folds)
        if scores is None:
            return False

        quick_score = scores[0]
        quick_duration = durations[0]

        score_state = MemberScoreState.get(member)

        score_state.quick_score = quick_score
        score_state.quick_duration = quick_duration
        score_state.quick_predictions = predictions

        score_state.scores = [ quick_score ]
        score_state.score = quick_score
        score_state.score_std = None

        score_state.score_durations =  [ quick_duration ]
        score_state.score_duration = quick_duration
        score_state.score_duration_std = None

        return True

    def evaluate_league_1(self, member):
        """
        Evaluate league 1 score by finishing of the quick score
        """
        folds = self.get_folds(member.get_specie(), 0, 1, self.n_splits)
        scores, durations, predictions = self.build_scores(member, folds)
        if scores is None:
            return False

        score_state = MemberScoreState.get(member)
        score_state.league_scores[1] = [ score_state.quick_score ] + scores
        score_state.league_durations[1] = [ score_state.quick_duration ] + durations
        quick_predictions = score_state.quick_predictions
        league_predictions = np.where(np.isnan(predictions), quick_predictions, predictions)
        score_state.league_predictions[1] = league_predictions
        return True

    def evaluate_league_scores(self, member, league):
        folds = self.get_folds(member.get_specie(), 0, 0, self.n_splits)
        scores, durations, predictions = self.build_scores(member, folds)
        if scores is None:
            return False

        score_state = MemberScoreState.get(member)
        score_state.league_scores[league] = scores
        score_state.league_durations[league] = durations
        score_state.league_predictions[league] = predictions
        return True

    def evaluate_scores(self, member):
        score_state = MemberScoreState.get(member)
        scores = np.concatenate([ score_state.league_scores[l] for l in score_state.league_scores ])
        score_state.scores = scores.tolist()
        score_state.score = np.mean(scores)
        score_state.score_std = np.std(scores)

        durations = np.concatenate([ score_state.league_durations[l] for l in score_state.league_durations ])
        score_state.score_durations = durations.tolist()
        score_state.score_duration = np.mean(durations)
        score_state.score_duration_std = np.std(durations)

    # Contests


    def contest_veterans(self, contestant1, contestant2):
        """
        Evaluate a contest between two veterans
        """

        contestant1_scores = MemberScoreState.get(contestant1)
        contestant2_scores = MemberScoreState.get(contestant2)

        # If scores are equal there is no outcome
        if contestant1_scores.get_score() == contestant2_scores.get_score():
            return
        winner = contestant1 if contestant1_scores.get_score() > contestant2_scores.get_score() else contestant2
        loser = contestant1 if contestant1_scores.get_score() < contestant2_scores.get_score() else contestant2
        winner.victory()
        loser.defeat()

    def contest_peers(self, contestant1, contestant2):
        """
        Evaluate a contest between peers, IE are at the same league but not veterans or rookies
        """

        contestant1_scores = MemberScoreState.get(contestant1)
        contestant2_scores = MemberScoreState.get(contestant2)

        # If scores are equal there is no outcome
        if contestant1_scores.get_score() == contestant2_scores.get_score():
            return

        pros = MemberLeagueState.get(contestant1).is_pro()
        # If the score of one contestant is inside the 60% confidence interval of the other then their is no outcome
        if pros and contestant1_scores.get_low_score() <= contestant2_scores.get_score() <= contestant1_scores.get_high_score():
            return

        # If the score of one contestant is inside the 95% confidence interval of the other then their is no outcome
        if not pros and contestant1_scores.get_lower_score() <= contestant2_scores.get_score() <= contestant1_scores.get_upper_score():
            return

        # Their is clear seperation so we can determine an outcome
        winner = contestant1 if contestant1_scores.get_score() > contestant2_scores.get_score() else contestant2
        loser = contestant1 if contestant1_scores.get_score() < contestant2_scores.get_score() else contestant2
        winner.victory()
        loser.defeat()

    def contest_mismatch(self, contestant1, contestant2):
        """
        Evaluate a mismatch, where the contestants are at different league levels
        """

        contestant1_leagues = MemberLeagueState.get(contestant1)
        contestant2_leagues = MemberLeagueState.get(contestant2)

        # Determine who is the senior and who is the junior
        senior = contestant1 if contestant1_leagues.get_league() > contestant2_leagues.get_league() else contestant2
        junior = contestant1 if contestant1_leagues.get_league() < contestant2_leagues.get_league() else contestant2
        pros = MemberLeagueState.get(junior).is_pro()

        # If scores are equal there is no outcome
        senior_scores = MemberScoreState.get(senior)
        junior_scores = MemberScoreState.get(junior)

        # If they are pros and the score of the junior is inside the 60% confidence interval of the senior then their is no outcome
        if pros and senior_scores.get_low_score() <= junior_scores.get_score() <= senior_scores.get_high_score():
            return

        # If they are not both pros and the score of the junior is inside the 95% confidence interval of the senior then their is no outcome
        if not pros and senior_scores.get_lower_score() <= junior_scores.get_score() <= senior_scores.get_upper_score():
            return

        # Their is clear seperation so we can determine an outcome
        winner = senior if senior_scores.get_score() > junior_scores.get_score() else junior
        loser = senior if senior_scores.get_score() < junior_scores.get_score() else junior
        winner.victory()
        loser.defeat()        

    def contest_members(self, contestant1, contestant2):

        specie = contestant1.get_specie()

        contestant1_leagues = MemberLeagueState.get(contestant1)
        contestant2_leagues = MemberLeagueState.get(contestant2)

        # If both members are rookies then the scores are too inaccurate to make a judgement
        if contestant1_leagues.is_rookie() and contestant2_leagues.is_rookie():
            return

        # If both members are veterans then we can use the veteran test
        if contestant1_leagues.is_veteran() and contestant2_leagues.is_veteran():
            self.contest_veterans(contestant1, contestant2)
            return

        # If both members are on the same league then we can use the peers test
        if contestant1_leagues.get_league() == contestant2_leagues.get_league():            
            self.contest_peers(contestant1, contestant2)
            return

        # Otherwise make the mismatch test
        self.contest_mismatch(contestant1, contestant2)

    def record_member(self, member, record):
        super().record_member(member, record)

        score_state = MemberScoreState.get(member)
        record.SE_score = score_state.score
        record.SE_score_std = score_state.score_std
