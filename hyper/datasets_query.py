from .configuration_query import ConfigurationQuery

import pandas

class DatasetQuery:
    """
    Queries relating to the hyper-analysis datasets
    """

    def __init__(self, hyper_analysis):
        self._hyper_analysis = hyper_analysis

    def get_hyper_analysis(self):
        """
        Get the underlying hyper analysis
        """
        return self._hyper_analysis

    def get_datasets(self):
        """
        Return a dataframe of all available datasets
        """
        configuration = ConfigurationQuery(self.get_hyper_analysis())
        df = pandas.read_excel(configuration.get_hyper_configuration_filename())
        df.rename(columns={'Name':'name', 'Status':'status'}, inplace=True)        
        df['active'] = df['status'] == "Run"
        return df
