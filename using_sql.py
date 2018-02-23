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

import sqlite3
from sqlite3 import Error

# Read in the data
df_list = []
directory = "./s3_files/seoul/" 
sqlite_file = directory + "db.sqlite"

for filename in os.listdir(directory):
  if filename[-3:] == 'csv':
    df_list.append(pd.read_csv(directory + filename))

df = pd.concat(df_list)

# See which columns have null values
df.isnull().sum()

# Clean out the null values
df = df[df['bedrooms'].notnull()]
df = df.loc[:, df.isnull().sum() == 0]

# Connect to sql
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Write to sql
df.to_sql("Housing", conn)


# Only use top 50 neighborhoods
sql_query = """
DELETE 
FROM Housing
WHERE neighborhood NOT IN 
(SELECT 
  h2.neighborhood 
FROM 
  Housing h2 
GROUP By
  h2.neighborhood
ORDER BY COUNT(*) DESC
LIMIT 50)
"""

c.execute(sql_query)  
c.fetchall()


# Look for one entry per (room_id, month, year)
sql_query = """
SELECT * 
FROM Housing
GROUP BY
  room_id, strftime('%m', last_modified), strftime('%Y', last_modified)
"""

c.execute(sql_query)  
data = c.fetchall()

# hack to stop 
stop

conn.commit()
conn.close()