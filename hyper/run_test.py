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
    study = hyper_analysis.get_study("linear")
    dataset = study.get_dataset("ada_agnostic")
    print(study.get_datasets_status())
