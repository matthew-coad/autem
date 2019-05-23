import benchmark.baselines

from pathlib import Path

class ConfigurationQuery:

    def __init__(self, hyper_analysis):
        self._hyper_analysis = hyper_analysis

    def get_hyper_analysis(self):
        return self._hyper_analysis

    def get_hyper_directory(self):
        return Path("hyper")

    def get_baselines_directory(self):
        return benchmark.baselines.baselines_directory()

    def get_hyper_configuration_filename(self):
        return self.get_hyper_directory().joinpath("Configuration.xlsx")

    def get_hyper_simulations_path(self):
        return self.get_hyper_directory().joinpath("Simulations")

    #def get_hyper_configuration_filename():
    #    return get_hyper_directory().joinpath("Configuration.xlsx")

    #def get_hyper_simulations_path():
    #    return get_hyper_directory().joinpath("Simulations")

    #def load_hyper_configuration_data():
    #    filename = get_hyper_configuration_filename()
    #    df = pandas.read_excel(filename)
    #    return df

    #def get_hyper_names(status = "Run"):
    #    df = load_hyper_configuration_data()
    #    dfa = df[df["Status"] == status]
    #    return dfa.Name

    #def get_hyper_configuration(name):
    #    df = load_hyper_configuration_data()
    #    dfa = df[df['Name'] == name]
    #    configuration = dfa.to_dict('records')[0]
    #    return configuration
