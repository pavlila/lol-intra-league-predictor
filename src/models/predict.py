import pickle
import pandas as pd
from pathlib import Path

def predict_winner(processed_df):
    model_path = Path(__file__).parent / "src" / "models" / "random_forest.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    prediction = model.predict_proba(processed_df)
    return prediction
