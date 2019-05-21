from ..simulation_manager import SimulationManager
from ..member_manager import MemberManager
from ..specie_manager import SpecieManager
from ..reporters import Reporter

from ..simulation_settings import SimulationSettings

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

    def __init__(self, metric, splits):
        SimulationManager.__init__(self)
        MemberManager.__init__(self)
        SpecieManager.__init__(self)
        Reporter.__init__(self)
        self._metric = metric
        self._splits = splits

        

    # Simulation

    # Specie

    def prepare_specie(self, specie):
        """
        Prepare folds
        """
        specie_score_state = SpecieScoreState.get(specie)
        specie_score_state.set_metric(self._metric)
        specie_score_state.set_splits(self._splits)

        self.prepare_folds(specie)

    def prepare_folds(self, specie):
        """
        Build the folds for a given specie
        """
        score_query = ScoreQuery(specie)
        n_folds = score_query.get_n_folds()
        n_repeats = score_query.get_n_repeats()
        random_state = SimulationSettings(specie).get_random_state()

        data = specie.get_simulation().get_training_data()
        features = data.features
        x = data.x
        y = data.y

        fold = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_repeats, random_state=random_state)
        folds = [ (i_train, i_test) for i_train, i_test in fold.split(x, y) ]

        specie_score_state = SpecieScoreState.get(specie)
        specie_score_state.set_folds(folds)
        return folds

    # Member

    def evaluate_member(self, member):

        score_query = MemberScoreQuery(member)

        if not score_query.has_league_scores(member.league):
            self.evaluate_league(member, member.league)

    def evaluate_league(self, member, league):

        score_query = MemberScoreQuery(member)
        score_state = MemberScoreState.get(member)

        ## Flatten into folds/repeat list
        splits = score_query.get_splits()
        split_repeats = [ (r[0], s) for r in enumerate(splits) for s in r[1] ]

        # Determine which repeat we are in
        repeat = split_repeats[league][0]

        # Determine the repeat start stop indexes
        repeat_start = next(sr[0] for sr in enumerate(split_repeats) if sr[1][0] == repeat)
        start_index = sum(sr[1] for sr in split_repeats[repeat_start:league])
        end_index = start_index + split_repeats[league][1]
        fold_indexes = range(start_index, end_index)

        league_state = MemberLeagueState(league)

        # Get prior league
        has_prior_league = league > 0
        prior_league = score_state.leagues[league-1] if has_prior_league else None

        # Evaluate fits
        fits = self.build_scores(member, fold_indexes)
        if fits is None:
            return False

        all_fits = prior_league.fits + fits if has_prior_league else fits
        league_state.fits = all_fits

        # Evaluate scores
        scores = [ f.score for f in fits ]
        scores = prior_league.scores + scores if has_prior_league else scores
        league_state.scores = scores
        league_state.score = np.mean(scores)
        league_state.score_std = np.std(scores)

        # Evaluate durations
        durations = [ f.duration for f in fits ]
        durations = prior_league.durations + durations if has_prior_league else durations
        league_state.durations = durations
        league_state.duration = np.mean(durations)
        league_state.duration_std = np.std(durations)

        # Build predictions
        data = member.get_simulation().get_training_data()
        y = data.y

        predictions = np.empty(len(y))
        predictions[:] = np.nan
        predictions = prior_league.predictions if has_prior_league else predictions

        folds = score_query.get_folds()
        for fit in fits:
            i_test = folds[fit.fold_index][1]
            predictions[i_test] = fit.predictions
        league_state.predictions = predictions

        # Save result
        score_state = MemberScoreState.get(member)
        score_state.leagues[league] = league_state
        score_state.current_league = league

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

    def record_member(self, member, record):
        super().record_member(member, record)

        score_state = MemberScoreQuery(member)
        record.SE_score = score_state.get_score()
        record.SE_score_std = score_state.get_score_std()
