from .container import Container
from .study import Study
from .configuration_query import ConfigurationQuery
import pandas

class HyperAnalysis(Container):

    def __init__(self, studies):
        Container.__init__(self)
        self._studies = studies
        for study in studies:
            study.set_parent(self)

    def get_datasets_status(self):
        """
        Return a dataframe of all available datasets
        """
        configuration = ConfigurationQuery(self)
        df = pandas.read_excel(configuration.get_hyper_configuration_filename())
        df.rename(columns={'Name':'name', 'Status':'status'}, inplace=True)        
        df['active'] = df['status'] == "Run"
        return df

    def get_study(self, name):
        return next((s for s in self._studies if s.get_name() == name), None)

