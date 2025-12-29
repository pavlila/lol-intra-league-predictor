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

data = pd.concat([train, val], ignore_index=True)

Xdata = data.drop(columns=['teamA_win'])
ydata = data['teamA_win']

Xdata['date'] = pd.to_datetime(Xdata['date'])

min_date = Xdata['date'].min()
max_date = Xdata['date'].max()
sample_weight = (Xdata['date'] - min_date) / (max_date - min_date)

Xdata = Xdata.drop(columns=['date'])

rf = RandomForestClassifier(n_estimators=18, max_depth=8, min_samples_leaf=1, min_samples_split=5, random_state=random_seed)
rf.fit(Xdata, ydata, sample_weight=sample_weight)

SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / "random_forest.pkl"

with open(MODEL_PATH, 'wb') as f:
    pickle.dump(rf, f)