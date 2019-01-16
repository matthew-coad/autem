import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(12345678)
rvs1 = stats.norm.rvs(loc=5,scale=1,size=20)
rvs2 = stats.norm.rvs(loc=5,scale=1,size=10)
rvs3 = stats.norm.rvs(loc=5.1,scale=1,size=10)

print(stats.ttest_ind(rvs1, rvs2))
print(stats.ttest_ind(rvs1, rvs3)) # positive if 1 > 2
print(stats.ttest_ind(rvs3, rvs1))

