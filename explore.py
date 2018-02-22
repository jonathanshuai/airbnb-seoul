# Skeleton file for basic exploratory analysis

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

train_file = "./data/train.csv"
test_file = "./data/test.csv"

train_df = pd.read_csv(train_file) 
test_df = pd.read_csv(test_file) 

