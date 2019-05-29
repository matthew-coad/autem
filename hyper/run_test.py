if __name__ == '__main__':
    import context

from hyper import HyperAnalysis
from hyper import ConfigurationQuery
from hyper import Study

if __name__ == '__main__':

    hyper_analysis = HyperAnalysis(studies = [ 
        Study("snapshot"),
        Study("linear"),
    ])
    print(hyper_analysis.get_study("snapshot").get_datasets_status())
