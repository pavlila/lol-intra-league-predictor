import streamlit as st
from pathlib import Path
import pickle

from process_new_data import processNewData

st.title("LOL Intra-League Predictor")

teamA = st.text_input("Team A Name")
teamB = st.text_input("Team B Name")

league = st.selectbox("Select League", ["LCS", "LEC", "LCK", "LPL"])

date = st.date_input("Match Date")

if st.button("Predict Winner"):
    model_path = Path(__file__).parent / "src" / "models" / "random_forest.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    