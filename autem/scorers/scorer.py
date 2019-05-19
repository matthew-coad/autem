from ..simulation_manager import SimulationManager
from ..member_manager import MemberManager
from ..specie_manager import SpecieManager
from ..reporters import Reporter

from ..simulation_settings import SimulationSettings
from .score_settings import ScoreSettings

from .member_score_state import MemberScoreState
from .specie_score_state import SpecieScoreState
from .member_league_state import MemberLeagueState
from .fit_state import FitState

from .score_query import ScoreQuery
from .member_score_query import MemberScoreQuery

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
        SpecieScoreState.get(specie).set_folds(folds)

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

        score_query = MemberScoreQuery(member)
        if member.league == 0 and not score_query.has_league_scores(0):
            self.evaluate_quick_score(member)
            return None

        # At league level 1 add on the complete scores
        evaluated = False
        if member.league == 1 and not score_query.has_league_scores(1):
            evaluated = self.evaluate_league_1(member)

        # High league levels
        if member.league > 1 and not score_query.has_league_scores(member.league):
            evaluated = self.evaluate_league_scores(member, member.league)

        if evaluated:
            self.evaluate_scores(member)

    def get_fold_indexes(self, specie, repeat, start, stop):
        start_index = self.n_splits * repeat + start
        end_index = self.n_splits * repeat + start + stop
        fold_indexes = range(start_index, end_index)
        return fold_indexes

    def build_scores(self, member, fold_indexes):
        """
        Build scores for the given member for the given folds
        """

        score_query = ScoreQuery(member)
        metric = score_query.get_metric()
        folds = score_query.get_folds()
        pipeline = member.get_pipeline()

        data = member.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        fits = []
        for fold_index in fold_indexes:

            fit = FitState()
            fits.append(fit)
            fit.fold_index = fold_index

            fold = folds[fold_index]
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
                    fit.fault = ex
                    member.fail(ex, "score_evaluator", "ScoreEvaluator")
                    return None
            end_time = time.time()
            duration = end_time - start_time
            score = metric(y_test, y_pred)

            fit.score = score
            fit.predictions = y_pred
            fit.duration = duration
        return fits

    def evaluate_quick_score(self, member):
        """
        Evaluate a quick score based on a single fit using the first entry in quick_fold
        """
        folds_index = self.get_fold_indexes(member.get_specie(), 0, 0, 1)
        fits = self.build_scores(member, folds_index)
        if fits is None:
            return False

        quick_score = fits[0].score
        quick_duration = fits[0].duration

        league_state = MemberLeagueState(0)
        league_state.fits = fits
        league_state.score = quick_score
        league_state.score_std = None
        league_state.duration = quick_duration
        league_state.duration_std = None
        league_state.predictions = None

        score_state = MemberScoreState.get(member)
        score_state.leagues[league_state.league] = league_state

        score_state.scores = [ quick_score ]
        score_state.score = quick_score
        score_state.score_std = None

        score_state.score_durations = [ quick_duration ]
        score_state.score_duration = quick_duration
        score_state.score_duration_std = None

        return True

    def complete_league_state(self, member, league, fits):
        score_query = ScoreQuery(member)
        folds = score_query.get_folds()

        league_state = MemberLeagueState(league)
        league_state.fits = fits

        scores = [ f.score for f in fits ]
        league_state.score = np.mean(scores)
        league_state.score_std = np.std(scores)

        durations = [ f.duration for f in fits ]
        league_state.duration = np.mean(durations)
        league_state.duration_std = np.std(durations)

        data = member.get_simulation().get_training_data()
        y = data.y

        predictions = np.empty(len(y))
        predictions[:] = np.nan
        for fit in fits:
            i_test = folds[fit.fold_index][1]
            predictions[i_test] = fit.predictions
        league_state.predictions = predictions

        score_state = MemberScoreState.get(member)
        score_state.leagues[league_state.league] = league_state

    def evaluate_league_1(self, member):
        """
        Evaluate league 1 score by finishing of the quick score
        """
        folds_index = self.get_fold_indexes(member.get_specie(), 0, 1, self.n_splits)
        fits = self.build_scores(member, folds_index)
        if fits is None:
            return False

        score_state = MemberScoreState.get(member)

        league0_state = score_state.leagues[0]
        fits = league0_state.fits + fits
        self.complete_league_state(member, 1, fits)

        return True

    def evaluate_league_scores(self, member, league):
        folds_index = self.get_fold_indexes(member.get_specie(), 0, 0, self.n_splits)
        fits = self.build_scores(member, folds_index)
        if fits is None:
            return False

        self.complete_league_state(member, league, fits)            
        return True

    def evaluate_scores(self, member):
        score_state = MemberScoreState.get(member)
        scores = [ f.score for l in score_state.leagues.values() for f in l.fits ]
        score_state.scores = scores
        score_state.score = np.mean(scores)
        score_state.score_std = np.std(scores)

        durations = [ f.duration for l in score_state.leagues.values() for f in l.fits ]
        score_state.score_durations = durations
        score_state.score_duration = np.mean(durations)
        score_state.score_duration_std = np.std(durations)

    # Contests


    def contest_veterans(self, contestant1, contestant2):
        """
        Evaluate a contest between two veterans
        """

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

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

        contestant1_scores = MemberScoreQuery(contestant1)
        contestant2_scores = MemberScoreQuery(contestant2)

        # If scores are equal there is no outcome
        if contestant1_scores.get_score() == contestant2_scores.get_score():
            return

        pros = contestant1_scores.is_pro()
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

        contestant1_leagues = MemberScoreQuery(contestant1)
        contestant2_leagues = MemberScoreQuery(contestant2)

        # Determine who is the senior and who is the junior
        senior = contestant1 if contestant1_leagues.get_league() > contestant2_leagues.get_league() else contestant2
        junior = contestant1 if contestant1_leagues.get_league() < contestant2_leagues.get_league() else contestant2
        pros = MemberScoreQuery(junior).is_pro()

        # If scores are equal there is no outcome
        senior_scores = MemberScoreQuery(senior)
        junior_scores = MemberScoreQuery(junior)

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

        contestant1_leagues = MemberScoreQuery(contestant1)
        contestant2_leagues = MemberScoreQuery(contestant2)

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

        score_state = MemberScoreQuery(member)
        record.SE_score = score_state.get_score()
        record.SE_score_std = score_state.get_score_std()
