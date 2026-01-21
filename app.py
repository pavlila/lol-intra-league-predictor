import streamlit as st
from pathlib import Path
import pandas as pd
from thefuzz import process, fuzz

from src.utils.process_data import LolDataProcessor
from src.utils.process_new_data import LoLDataNewProcessor
from src.models.predict import LoLPredictor

class LoLPredictorApp:
    """
    A Streamlit web application that provides a user interface for 
    the League of Legends match predictor.
    """

    def __init__(self):
        """
        Initializes the application, sets the page title, and 
        instantiates the required logic components.
        """
        st.set_page_config(page_title="LOL Predictor", layout="centered")
        self.processor = LolDataProcessor()
        self.processor_new = LoLDataNewProcessor()
        self.predictor = LoLPredictor()

        BASE_DIR = Path(__file__).resolve().parent
        self.teams_name_path = BASE_DIR / "data" / "merged" / "data.csv"
        
        self.team_league_map = {}
        self.valid_teams = self._load_team_and_league_list()

    def _load_team_and_league_list(self):
        """
        Loads the list of valid team names and leagues from the dataset.
        """
        df = pd.read_csv(self.teams_name_path)
        for _, row in df.iterrows():
            self.team_league_map[row["teamA"]] = row["league"]
            self.team_league_map[row["teamB"]] = row["league"]
        return list(self.team_league_map.keys())
    
    def _get_best_match(self, user_input):
        """
        Uses fuzzy matching to find the closest valid team name to the user input.
        """
        if not user_input or not self.valid_teams:
            return None, 0
        best_match, score = process.extractOne(user_input, self.valid_teams, scorer=fuzz.ratio)
        return best_match, score
    
    def _process_ui_logic(self, team_a_input, team_b_input, league, date):
        """
        Processes user inputs and triggers prediction logic.
        """
        if not team_a_input or not team_b_input:
            st.error("Please enter both team names.")
            return
        
        team_a, score_a = self._get_best_match(team_a_input)
        team_b, score_b = self._get_best_match(team_b_input)

        threshold = 70
        if score_a < threshold or score_b < threshold:
            st.error("One or both team names are not recognized. Please check your input.")

            col_err1, col_err2 = st.columns(2)
            with col_err1:
                st.info(f"Best match for A: **{team_a}** ({score_a}%)")
            with col_err2:
                st.info(f"Best match for B: **{team_b}** ({score_b}%)")
            return

        league_a = self.team_league_map.get(team_a)
        league_b = self.team_league_map.get(team_b)

        if league_a != league or league_b != league:
            st.error(f"One of the teams does not belong to the selected league (**{league}**).")
            if league_a != league:
                st.warning(f"**{team_a}** plays in **{league_a}**")
            if league_b != league:
                st.warning(f"**{team_b}** plays in **{league_b}**")
            return

        if team_a != team_a_input or team_b != team_b_input:
            st.info(f"Interpreting input as: **{team_a}** vs **{team_b}**")

        self._handle_prediction(team_a, team_b, league, date)

    def run(self):
        """
        Renders the Streamlit UI and handles user interactions.
        """
        st.title("LOL Intra-League Predictor")
        st.subheader("Predict outcomes of upcoming professional matches")

        with st.sidebar:
            st.header("Admin Tools")
            if st.button("Run Data Processing Pipeline"):
                with st.spinner("Processing historical data..."):
                    self.processor.run_pipeline()
                    st.success("Pipeline finished!")

        col1, col2 = st.columns(2)
        with col1:
            team_a_input = st.text_input("Team A Name", placeholder="e.g. T1")
        with col2:
            team_b_input = st.text_input("Team B Name", placeholder="e.g. Gen.G")

        league = st.selectbox("Select League", ["LEC", "LCK", "LPL", "LTA N", "LTA S", "LCP"])
        date = st.date_input("Match Date")

        if st.button("Predict Winner", use_container_width=True):
            self._process_ui_logic(team_a_input, team_b_input, league, date)

        st.markdown("""
        ---
        The model is trained on historical match data up to 2025, with the final matches of each league excluded.

        For realistic evaluation, the following matches represent the last matches played in each league:

        * Movistar KOI vs. G2 Esports (LEC, 2025-09-28) -> in reality, G2 Esports won

        * Hanwha Life Esports vs. Gen.G (LCK, 2025-09-28) -> in reality, Gen.G won

        * Invictus Gaming vs. JD Gaming (LPL, 2025-09-27) -> in reality, Invictus Gaming won
                    
        * FlyQuest vs. 100 Thieves (LTA N, 2025-09-07) -> in reality, FlyQuest won
                    
        * RED Canids vs. Vivo Keyd Stars (LTA S, 2025-09-07) -> in reality, Vivo Keyd Stars won
                    
        * CTBC Flying Oyster vs. Team Secret Whales (LCP, 2025-09-21) -> in reality, CTBC Flying Oyster won

        """)

    def _handle_prediction(self, team_a, team_b, league, date):
        """
        Internal method to process data and display prediction results.
        """
        match_df = pd.DataFrame([{
            "teamA": team_a,
            "teamB": team_b,
            "league": league,
            "date": pd.to_datetime(date),
        }])

        with st.spinner("Analyzing stats..."):
            processed_df = self.processor_new.run_pipeline(match_df)
            
            prediction = self.predictor.predict_winner(processed_df)
            probability = self.predictor.predict_winner_probability(processed_df)

        st.divider()
        result_label = "WIN" if prediction[0] == 1 else "LOSS"
        st.metric(label=f"Prediction for {team_a}", value=result_label)
        
        prob_val = probability[0][1]
        st.write(f"Winning Probability: {prob_val:.2f}")
        
        if prediction[0] == 1:
            st.success(f"The model predicts that **{team_a}** will win against **{team_b}**.")
        else:
            st.error(f"The model predicts that **{team_a}** will lose against **{team_b}**.")

if __name__ == "__main__":
    app = LoLPredictorApp()
    app.run()