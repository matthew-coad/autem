if __name__ == '__main__':
    import context

from hyper import HyperAnalysis
from hyper import ConfigurationQuery
from hyper import DatasetQuery

if __name__ == '__main__':

    hyper_analysis = HyperAnalysis()
    data = DatasetQuery(hyper_analysis)
    print(data.get_datasets())
