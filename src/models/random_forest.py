import math
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
import pickle

from pathlib import Path

random_seed = 42

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "featured" 

train = pd.read_csv(DATA_PATH / "train.csv", sep=',')
val = pd.read_csv(DATA_PATH / "val.csv", sep=',')

Xtrain = train.drop(columns=['teamA_win'])
ytrain = train['teamA_win']

Xval = val.drop(columns=['teamA_win'])
yval = val['teamA_win']

Xtrain['date'] = pd.to_datetime(Xtrain['date'])
Xval['date'] = pd.to_datetime(Xval['date'])

min_date = Xtrain['date'].min()
max_date = Xtrain['date'].max()
sample_weight = (Xtrain['date'] - min_date) / (max_date - min_date)

Xtrain = Xtrain.drop(columns=['date'])
Xval = Xval.drop(columns=['date'])

rf = RandomForestClassifier(n_estimators=18, max_depth=8, min_samples_leaf=1, min_samples_split=5, random_state=random_seed)
rf.fit(Xtrain, ytrain, sample_weight=sample_weight)

SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / "random_forest.pkl"

with open(MODEL_PATH, 'wb') as f:
    pickle.dump(rf, f)