import openml
import numpy as np
import pandas as pd

# Read data
df = pd.read_csv('D:\\Documents\\autem\\benchmark\\simulations\\quick\\profb\\battle.csv', low_memory=False)

df = df[df["alive"] == 0]
df = df[~df["score"].isna()]

# Reduce to final values
df = df.loc[:, ['study', 'experiment','step','member_id', 'event', 'final', 'score','Scaler','Selector','Reducer','Approximator', 'Learner']]

print(df)
print(df.shape)
