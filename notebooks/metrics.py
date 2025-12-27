import sklearn.metrics as metrics
import numpy as np
import matplotlib.pyplot as plt

def print_metrics(y_true, y_pred, y_proba):
    accuracy = metrics.accuracy_score(y_true, y_pred)
    conf_matrix = metrics.confusion_matrix(y_true, y_pred)
    f1 = metrics.f1_score(y_true, y_pred)
    
    print(f'Accuracy: {accuracy}')
    print('Confusion Matrix:')
    print(conf_matrix)
    print(f'F1 Score: {f1}')
    
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_proba)

    j_scores = tpr - fpr
    best_idx = np.argmax(j_scores)
    best_threshold = thresholds[best_idx]
    print(f'Best Threshold (Youden\'s J statistic): {best_threshold}')

    plt.figure(figsize=(6, 6))

    AUC = metrics.roc_auc_score(y_true, y_proba)

    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.plot(fpr, tpr, color="darkorange", lw=2, label = f"ROC křivka (AUC = {AUC:.3f})")
    plt.scatter(fpr[best_idx], tpr[best_idx], color='red', label=f'Nejlepší práh = {best_threshold:.3f}')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC křivka")
    plt.legend(loc="lower right")
    plt.show()