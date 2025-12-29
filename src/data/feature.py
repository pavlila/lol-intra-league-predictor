import pandas as pd


class LoLDataFeatureEngineer:
    """
    A class for feature engineering and dataset preparation.
    It creates differential features and splits data into training and validation sets.
    """

    def __init__(self):
        pass

    def make_mirror_matches(self, df):
        """
        Doubles the dataset by creating 'mirrored' versions of each match.
        For every match (Team A vs Team B), it adds a row for (Team B vs Team A).
        This helps the model learn that the order of teams does not matter.

        Args:
            df (pd.DataFrame): The original match dataset.

        Returns:
            pd.DataFrame: A dataset with twice the number of rows (original + mirrored).
        """

        df_orig = df.copy()
        df_mirror = df.copy()

        a_cols = [c for c in df.columns if c.endswith("_A")]
        for a_col in a_cols:
            base = a_col[:-2]
            b_col = f"{base}_B"
            df_mirror[a_col], df_mirror[b_col] = df[b_col], df[a_col]

        df_mirror["teamA"], df_mirror["teamB"] = df["teamB"], df["teamA"]

        df_mirror["teamA_win"] = 1 - df["teamA_win"]

        df_out = pd.concat([df_orig, df_mirror], ignore_index=True)

        return df_out

    def make_diff(self, df):
        """
        Transforms raw stats of two teams into comparative features.
        Calculates the difference (A - B) and the ratio (A / B) for all metrics.

        Args:
            df (pd.DataFrame): DataFrame with separate columns for Team A and Team B.

        Returns:
            pd.DataFrame: DataFrame containing only comparative features (diffs and ratios),
                         with original team-specific columns removed.
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

    def make_feature(self, df, validation=1):
        """
        Main pipeline for preparing training and validation datasets.
        Splits data by date, augments the training set, and creates features.

        Args:
            df (pd.DataFrame): The merged dataset with all match and team info.
            validation (int): Number of months from the end of the dataset to use for validation.

        Returns:
            tuple: (train_df, val_df) - Two DataFrames ready for machine learning.
        """
        df["date"] = pd.to_datetime(df["date"])

        max_date = df["date"].max()
        validation_start = max_date - pd.DateOffset(months=validation)

        train_df = df[df["date"] < validation_start].copy()
        val_df = df[df["date"] >= validation_start].copy()

        train_df = self.make_mirror_matches(train_df)

        meta_cols = ["teamA", "teamB", "league"]

        train_df = self.make_diff(train_df.drop(columns=meta_cols, errors="ignore"))
        val_df = self.make_diff(val_df.drop(columns=meta_cols, errors="ignore"))

        train_df = train_df.fillna(-1)
        val_df = val_df.fillna(-1)

        return train_df, val_df
