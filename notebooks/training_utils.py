import sklearn.metrics as metrics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def print_metrics(y_true, y_pred, y_proba):
    """
    Calculates and visualizes key performance metrics for a classification model.

    This function prints the accuracy score, confusion matrix, and F1 score.
    It also determines the optimal classification threshold using Youden's J statistic
    and plots the Receiver Operating Characteristic (ROC) curve.

    Args:
        y_true (array-like): Ground truth (correct) target values.
        y_pred (array-like): Estimated targets as returned by a classifier.
        y_proba (array-like): Predicted probabilities for the positive class
                              (typically the second column of model.predict_proba).

    Returns:
        None
    """
    accuracy = metrics.accuracy_score(y_true, y_pred)
    conf_matrix = metrics.confusion_matrix(y_true, y_pred)
    f1 = metrics.f1_score(y_true, y_pred)

    print(f"Accuracy: {accuracy}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print(f"F1 Score: {f1}")

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_proba)

    j_scores = tpr - fpr
    best_idx = np.argmax(j_scores)
    best_threshold = thresholds[best_idx]
    print(f"Best Threshold (Youden's J statistic): {best_threshold}")

    plt.figure(figsize=(6, 6))

    AUC = metrics.roc_auc_score(y_true, y_proba)

    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC křivka (AUC = {AUC:.3f})")
    plt.scatter(
        fpr[best_idx],
        tpr[best_idx],
        color="red",
        label=f"Nejlepší práh = {best_threshold:.3f}",
    )
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC křivka")
    plt.legend(loc="lower right")
    plt.show()


def prepare_dataset():
    """
    Loads data, extracts target variables, and calculates time-based sample weights for training.

    Returns:
        tuple: (Xtrain, ytrain, Xval, yval, sample_weight)
    """
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data" / "featured"
    train_path = data_dir / "train.csv"
    val_path = data_dir / "val.csv"
    train = pd.read_csv(train_path, sep=",")
    val = pd.read_csv(val_path, sep=",")

    train["date"] = pd.to_datetime(train["date"])
    min_date = train["date"].min()
    max_date = train["date"].max()

    sample_weight = (train["date"] - min_date) / (max_date - min_date)

    ytrain = train["teamA_win"]
    Xtrain = train.drop(columns=["teamA_win", "date"])

    yval = val["teamA_win"]
    Xval = (
        val.drop(columns=["teamA_win", "date"])
        if "date" in val.columns
        else val.drop(columns=["teamA_win"])
    )

    return Xtrain, ytrain, Xval, yval, sample_weight
