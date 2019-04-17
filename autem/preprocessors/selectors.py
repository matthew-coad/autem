from .. import Group, Dataset, Role, ChoicesParameter

import sklearn.impute
import sklearn.preprocessing
import sklearn.decomposition
import sklearn.compose
import sklearn.cluster
import sklearn.kernel_approximation
import sklearn.feature_selection
import sklearn.pipeline

import numpy as np

from .preprocessor import Preprocesssor

# Feature Selectors

class Selector(Preprocesssor):

    def __init__(self, name, label, parameters):
        Preprocesssor.__init__(self, name, label, parameters)

class NoSelector(Selector):

    def __init__(self):
        Selector.__init__(self, "LNO", "No Selector", [])

    def make_preprocessor(self, member):
        return None

class SelectPercentile(Selector):

    def __init__(self):
        scorer_parameter = ChoicesParameter("scorer", "scorer", 'nominal', ['f_classif', 'mutual_info_classif', 'chi2'])
        percentile_parameter = ChoicesParameter("percentile", "percentile", 'numeric', [1,2,5,10,20,30,40,50,60,70,80,90,95,100])
        Selector.__init__(self, "LPC", "Select Percentile", [scorer_parameter, percentile_parameter])

    def make_preprocessor(self, member):
        scorer_param = self.get_parameter("scorer")
        scorer = scorer_param.get_value(member)
        scorer = scorer if scorer is not None else "f_classif"
        scorer_param.set_value(member, scorer)

        percentile_param = self.get_parameter("percentile")
        percentile = percentile_param.get_value(member)
        percentile = percentile if percentile is not None else 10
        percentile_param.set_value(member, percentile)

        if scorer == "f_classif":
            score_func = sklearn.feature_selection.f_classif
        elif scorer == "mutual_info_classif":
            score_func = sklearn.feature_selection.mutual_info_classif
        elif scorer == "chi2":
            score_func = sklearn.feature_selection.chi2
        else:
            raise RuntimeError("No scorer selected")
        selector = sklearn.feature_selection.SelectPercentile(score_func=score_func, percentile=percentile)
        return selector

    def configure_preprocessor(self, member, pre_processor):
        pass

    def update_parameters(self, member, pre_processor):
        pass

class VarianceThreshold(Selector):

    def __init__(self):
        threshold_parameter = ChoicesParameter("threshold", "threshold", "numeric", [0.0, 0.05, 0.1, 0.15, 0.2])
        Selector.__init__(self, "LVT", "Variance Threshold", [threshold_parameter])

    def make_preprocessor(self, member):
        return sklearn.feature_selection.VarianceThreshold()
