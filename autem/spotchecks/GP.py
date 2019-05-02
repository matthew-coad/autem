from .decision_model_manager import DecisionModelManager
from ..component_state import ComponentState

from scipy import stats

from sklearn.pipeline import Pipeline
from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as kernels
from sklearn.preprocessing import OneHotEncoder


class GP(DecisionModelManager):
    """
    Spotchecker that uses gaussian processes model
    """

    def __init__(self):
        DecisionModelManager.__init__(self)

    def build_model(self, simulation, decisions_df):
        """
        Build the model using GP
        """

        # Get the data

        # Extract the choices as the response variables
        choices = ComponentState.get(simulation).list_choices()
        choice_names = [ c.get_name() for c in choices ]
        x = decisions_df.loc[:, choice_names]

        # Extract the scores as the dependant variables
        y = decisions_df.loc[:, "score"]

        # Preprocess using one hot encoding
        categories = [ c.get_component_names() for c in choices ]
        encoder = OneHotEncoder(sparse = False, categories = categories)

        # Define the isotropic kernel
        kernel = 1.0 * kernels.RBF([5]) + kernels.WhiteKernel()

        # Define the regressor
        regressor = GaussianProcessRegressor(kernel=kernel, normalize_y = True)

        # Build the pipeline and fit it
        pipeline = Pipeline(steps = [
            ('encoder', encoder),
            ('regressor', regressor)
        ])
        pipeline.fit(x, y)
        return pipeline

