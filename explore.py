# Skeleton file for basic exploratory analysis

import os
import datetime
import numpy as np
import pandas as pd
import scipy.optimize
import scipy.stats

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

import matplotlib as mpl
from matplotlib import pyplot as plt
import hedgeplot as hplt


# Read in the data
df_list = []
directory = "./s3_files/seoul/" 
for filename in os.listdir(directory):
  if filename[-3:] == 'csv':
    df_list.append(pd.read_csv(directory + filename))

df = pd.concat(df_list)

# See which columns have null values
df.isnull().sum()

# Clean out the null values
df = df[df['bedrooms'].notnull()]
df = df.loc[:, df.isnull().sum() == 0]

# Work with only the top 50 neighborhoods
top_neighborhoods = df.groupby('neighborhood').count().sort_values(by='room_id').tail(50).index
df[df['neighborhood'].isin(top_neighborhoods)]

# remove seconds and hours from last_modified
# df['last_modified'] = df['last_modified'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f').date()) 

# try to group by month
df.index = df['last_modified']
df.index = pd.to_datetime(df.index)

month_groups = df.groupby(pd.Grouper(freq='m')).mean().tail(8)
df.groupby(pd.Grouper(freq='m')).mean()


x = month_groups.index
y = month_groups['price']

# Plot some time series
fig, ax = hplt.create_plot()
hplt.plot(x, y)
hplt.title("Price trend")
hplt.xlabel("Year-Month")
hplt.ylabel("Price in $US per night")
hplt.show()

# Some worries about this plot: not sure how the sampling was done, but if
# not random, no assumptions can be made about the price trend


# Check the trends for a single house
# df.groupby('room_id').count().sort_values('reviews').tail()
