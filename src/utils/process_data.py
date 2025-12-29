from src.data.clean import LoLDataCleaner
from src.data.merge import LoLDataMerger
from src.data.feature import LoLDataFeatureEngineer
import pandas as pd
import os
from pathlib import Path


class LolDataProcessor:
    """
    Orchestrates the entire data processing pipeline for League of Legends data.
    It coordinates cleaning, merging, and feature engineering steps.
    """

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.clean_dir = self.base_dir / "data" / "cleaned"
        self.merge_dir = self.base_dir / "data" / "merged"
        self.feature_dir = self.base_dir / "data" / "featured"

        self.cleaner = LoLDataCleaner()
        self.merger = LoLDataMerger()
        self.feature_engineer = LoLDataFeatureEngineer()

    def run_pipeline(self, years=["2023", "2024", "2025"], validation=2):
        """
        Executes the full pipeline:
        1. Cleans raw match and team data.
        2. Merges team statistics with match results.
        3. Engineers features and splits data into train/validation sets.

        Args:
            years (list): List of years to process.
            validation_months (int): Size of the validation set in months.

        Returns:
            None
        """
        matches = pd.concat(
            [self.cleaner.clean_matches(year) for year in years], ignore_index=True
        )
        teams = self.cleaner.clean_teams()

        matches["date"] = pd.to_datetime(matches["date"])
        teams["date"] = pd.to_datetime(teams["date"])

        matches.to_csv(os.path.join(self.clean_dir, "matches.csv"), index=False)
        teams.to_csv(os.path.join(self.clean_dir, "teams.csv"), index=False)

        data = self.merger.merge_teams_and_matches(matches, teams)
        data.to_csv(os.path.join(self.merge_dir, "data.csv"), index=False)

        train_df, val_df = self.feature_engineer.make_feature(
            data, validation=validation
        )
        train_df.to_csv(os.path.join(self.feature_dir, "train.csv"), index=False)
        val_df.to_csv(os.path.join(self.feature_dir, "val.csv"), index=False)

        return None
