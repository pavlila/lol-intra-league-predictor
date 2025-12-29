from src.data.clean_new_data import LoLNewDataCleaner
import pandas as pd
from pathlib import Path
from src.data.feature_new_data import LoLNewDataFeatureEngineer
from src.data.merge_new_data import LoLNewDataMerger


class LoLDataNewProcessor:
    """
    Orchestrates the processing of new match data for real-time predictions.
    It coordinates cleaning, merging, and feature engineering for upcoming fixtures.
    """

    def __init__(self):
        """
        Initializes the processor and sets up the base directory for data access.
        """
        self.base_dir = Path(__file__).resolve().parents[2]
        self.teams_data_path = self.base_dir / "data" / "cleaned"

        self.cleaner = LoLNewDataCleaner()
        self.merger = LoLNewDataMerger()
        self.feature_engineer = LoLNewDataFeatureEngineer()

    def run_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main execution method to transform raw new match data into model-ready features.

        Args:
            df (pd.DataFrame): Raw input data of upcoming matches.

        Returns:
            pd.DataFrame: A final feature set (differences and ratios) ready for prediction.
        """

        cleaned_df = self.cleaner.clean_new_matches(df)

        teams = pd.read_csv(self.teams_data_path / "teams.csv")
        teams["date"] = pd.to_datetime(teams["date"])

        merged_df = self.merger.merge_new_teams_and_matches(cleaned_df, teams)
        featured_df = self.feature_engineer.makeNewFeature(merged_df)
        featured_df = featured_df.drop(columns=["date"], errors="ignore")
        return featured_df
