import pandas as pd


class LoLNewDataCleaner:
    """
    A specialized cleaner for processing new or upcoming matches where
    the outcome is not yet known. Used primarily for making real-time predictions.
    """

    def __init__(self):
        """
        Initializes the cleaner with a mapping to standardize team names.
        """
        self.replace_map = {
            "Edward Gaming": "EDward Gaming",
            "Hanwha Life eSports": "Hanwha Life Esports",
            "TALON": "PSG Talon",
            "BNK FearX": "BNK FEARX",
            "GIANTX": "GiantX",
            "OMG": "Oh My God",
            "Fluxo": "Fluxo W7M",
            "Gen.G eSports": "Gen.G",
            "Anyone s Legend": "Anyone's Legend",
            "Isurus Estral": "Isurus",
            "Funplus Phoenix": "FunPlus Phoenix",
            "OK BRION": "OKSavingsBank BRION",
            "TT": "ThunderTalk Gaming",
        }

    def rename_teams_in_matches(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes team names in the DataFrame to ensure consistency
        with historical datasets.

        Args:
            df (pd.DataFrame): DataFrame with raw team names.

        Returns:
            pd.DataFrame: DataFrame with corrected team names.
        """
        df[["teamA", "teamB"]] = df[["teamA", "teamB"]].replace(self.replace_map).copy()
        return df

    def clean_new_matches(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and formats a DataFrame of new matches.
        It strips column names, selects relevant features, and converts dates.

        Args:
            df (pd.DataFrame): Raw input data of upcoming matches.

        Returns:
            pd.DataFrame: A formatted DataFrame ready for the merging process.
        """
        df.columns = df.columns.str.strip()

        df = df[["teamA", "teamB", "date", "league"]].copy()

        df = self.rename_teams_in_matches(df)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        return df
