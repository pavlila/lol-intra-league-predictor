from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class RF:
    """
    A class used to manage the training process of a RandomForest model for LoL predictions.
    """

    def __init__(self, random_seed=42):
        """
        Initializes the ModelTrainer with default paths and model hyperparameters.
        """
        self.random_seed = random_seed
        self.base_dir = Path(__file__).resolve().parents[2]
        self.data_path = self.base_dir / "data" / "featured"
        self.model_path = Path(__file__).parent / "random_forest.pkl"
        self.model = RandomForestClassifier(
            n_estimators=40,
            max_depth=8,
            min_samples_leaf=1,
            min_samples_split=6,
            random_state=self.random_seed,
        )

    def load_and_prepare_data(self):
        """
        Loads training and validation datasets, merges them, and calculates time-based sample weights.

        Returns:
            tuple: (X, y, sample_weight) where X is the feature set, y is the target,
                   and sample_weight is a Series of weights based on the match date.
        """
        train = pd.read_csv(self.data_path / "train.csv", sep=",")
        val = pd.read_csv(self.data_path / "val.csv", sep=",")
        data = pd.concat([train, val], ignore_index=True)

        Xdata = data.drop(columns=["teamA_win"])
        ydata = data["teamA_win"]

        Xdata["date"] = pd.to_datetime(Xdata["date"])

        min_date = Xdata["date"].min()
        max_date = Xdata["date"].max()
        sample_weight = (Xdata["date"] - min_date) / (max_date - min_date)

        Xdata = Xdata.drop(columns=["date"])

        return Xdata, ydata, sample_weight

    def train_and_save(self):
        """
        Executes the full workflow: loading data, training the model, and exporting the result as a pickle file.
        """
        Xdata, ydata, sample_weight = self.load_and_prepare_data()
        self.model.fit(Xdata, ydata, sample_weight=sample_weight)

        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)


if __name__ == "__main__":
    rf = RF()
    rf.train_and_save()
