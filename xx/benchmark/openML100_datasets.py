if __name__ == '__main__':
    import context

from pathlib import Path
import config
import openml
import os
import pandas as pd

def get_data_path():
    return Path("benchmark/data")

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')

def get_OpenML_List():
    prepare_OpenML()
    openml_list = openml.datasets.list_datasets(tag = 'OpenML100')
    df = pd.DataFrame.from_dict(openml_list, orient='index')
    return df

def download_OpenML100_datasets():
    df = get_OpenML_List()
    df.to_csv(get_data_path().joinpath("OpenML100_datasets.csv"))

def download_Benchmark_datasets():
    df = get_OpenML_List()
    bdf = df.query('NumberOfInstances < 10000 and NumberOfFeatures <= 20 and NumberOfClasses <= 10 and NumberOfMissingValues == 0')
    bdf.to_csv(get_data_path().joinpath("Benchmark_datasets.csv"))

def download_Dataset(bid):
    dataset = openml.datasets.get_dataset(bid)
    X, y, attribute_names = dataset.get_data(target=dataset.default_target_attribute, return_attribute_names=True,)
    df = pd.DataFrame(X, columns=attribute_names)
    df['class'] = y
    df_path = get_data_path().joinpath("%s.csv" % (dataset.name))
    df.to_csv(df_path)
    return df

if __name__ == '__main__':
    #download_OpenML100_datasets()
    download_Benchmark_datasets()
    #download_Dataset(11)
