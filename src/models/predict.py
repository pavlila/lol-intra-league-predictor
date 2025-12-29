import pickle
from pathlib import Path


class LoLPredictor:
    """
    A class used to load a trained machine learning model and perform
    winner predictions on processed League of Legends match data.
    """

    def __init__(self, model_name="random_forest.pkl"):
        """
        Initializes the predictor by loading the saved model from a file.

        Args:
            model_name (str): The filename of the pickled model.
        """
        self.model_path = Path(__file__).parent / model_name
        self.model = self._load_model()

    def _load_model(self):
        """
        Internal method to safely load the pickle file.
        """
        with open(self.model_path, "rb") as f:
            return pickle.load(f)

    def predict_winner_probability(self, processed_df):
        """
        Predicts the probability of victory for the competing teams.

        Args:
            processed_df (pd.DataFrame): Data containing comparative features
                                        (diffs and ratios) for the matches.

        Returns:
            np.ndarray: An array of probabilities for each class (e.g., [Loss, Win]).
        """
        return self.model.predict_proba(processed_df)

    def predict_winner(self, processed_df):
        """
        Predicts the final winner (0 or 1) for the matches.

        Args:
            processed_df (pd.DataFrame): Data containing comparative features.

        Returns:
            np.ndarray: An array of binary predictions (1 = Team A wins, 0 = Team B wins).
        """
        return self.model.predict(processed_df)
