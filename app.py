import streamlit as st
from pathlib import Path
import pickle
import pandas as pd

from utils.process_new_data import processNewData
from models.predict import predict_winner

st.title("LOL Intra-League Predictor")

teamA = st.text_input("Team A Name")
teamB = st.text_input("Team B Name")

league = st.selectbox("Select League", ["LCS", "LEC", "LCK", "LPL"])

date = st.date_input("Match Date")

if st.button("Predict Winner"):

    df = pd.DataFrame([{
        "teamA": teamA,
        "teamB": teamB,
        "league": league,
        "date": pd.to_datetime(date)
    }])

    processed_df = processNewData(df)

    prediction = predict_winner(processed_df)
    st.write(f"Prediction (Probability Team A wins): {prediction[0][1]:.2f}")

