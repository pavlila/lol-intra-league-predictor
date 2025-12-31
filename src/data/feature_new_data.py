import pandas as pd


class LoLNewDataFeatureEngineer:
    """
    A class to engineer features for new match predictions.
    It transforms raw team statistics into comparative metrics (differences and ratios).
    """

    def __init__(self):
        """
        Initializes the Feature Engineer for new data.
        """
        pass

    def makeDiff(self, df):
        """
        Calculates the differences and ratios between Team A and Team B stats.
        Removes the original columns to keep only the comparative features.

        Args:
            df (pd.DataFrame): Data with columns ending in _A and _B.

        Returns:
            pd.DataFrame: Data with 'diff_' and 'ratio_' features.
        """
        a_cols = [c for c in df.columns if c.endswith("_A")]
        diff_data = {}
        ratio_data = {}

        for a_col in a_cols:
            base = a_col[:-2]
            b_col = f"{base}_B"
            if b_col in df.columns:
                diff_data[f"diff_{base}"] = df[a_col] - df[b_col]
                ratio_data[f"ratio_{base}"] = df[a_col] / (df[b_col] + 1e-6)

        df = pd.concat([df, pd.DataFrame(diff_data), pd.DataFrame(ratio_data)], axis=1)
        drop_cols = [c for c in df.columns if c.endswith("_A") or c.endswith("_B")]
        df = df.drop(columns=drop_cols)
        return df

    def makeNewFeature(self, df):
        """
        Processes new matches into a format compatible with the trained model.
        Removes metadata and applies the differential transformation.

        Args:
            df (pd.DataFrame): Merged data of new matches with historical stats.

        Returns:
            pd.DataFrame: Features ready for model prediction.
        """
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        meta_cols = ["teamA", "teamB", "league"]

        df = self.makeDiff(df.drop(columns=meta_cols, errors="ignore"))

        return df
