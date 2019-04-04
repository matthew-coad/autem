if __name__ == '__main__':
    import context

import tests.config as config
from pandas import read_csv    

def test_datasets_path():
    return config.tests_path().joinpath("data")

# Load boston dataset
def load_boston():
    filename = test_datasets_path().joinpath('housing.csv')
    names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    df = read_csv(filename, delim_whitespace=True, names=names)
    array = df.values
    x = array[:,0:13]
    y = array[:,13]
    return (x,y)

# Load iris dataset
def load_iris():
    filename = test_datasets_path().joinpath('iris.data.csv')
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    df = read_csv(filename, names=names)
    array = df.values
    y = array[:,4]
    numeric_x = array[:,0:4]
    return (y, numeric_x)
