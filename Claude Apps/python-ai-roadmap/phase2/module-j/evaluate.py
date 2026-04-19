import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score,
    f1_score,
)

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def get_metrics(model, X_test, y_test) -> dict:
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    return {
        "f1":     f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "avg_precision": average_precision_score(y_test, y_proba),
        "report": classification_report(y_test, y_pred, output_dict=True),
        "cm":     confusion_matrix(y_test, y_pred),
        "y_pred": y_pred,
        "y_proba": y_proba,
    }


def plot_confusion_matrix(cm: np.ndarray, save: bool = True) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    fig.colorbar(im, ax=ax)
    classes = ["No Churn", "Churn"]
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(classes); ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black",
                    fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save:
        fig.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=150)
    return fig


def plot_roc_curve(y_test, y_proba, auc: float, save: bool = True) -> plt.Figure:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, lw=2, label=f"ROC (AUC = {auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random")
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve"); ax.legend()
    plt.tight_layout()
    if save:
        fig.savefig(REPORTS_DIR / "roc_curve.png", dpi=150)
    return fig


def plot_pr_curve(y_test, y_proba, ap: float, save: bool = True) -> plt.Figure:
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(recall, precision, lw=2, label=f"PR (AP = {ap:.3f})")
    ax.axhline(y_test.mean(), color="k", linestyle="--", lw=1,
               label=f"Baseline ({y_test.mean():.2f})")
    ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve"); ax.legend()
    plt.tight_layout()
    if save:
        fig.savefig(REPORTS_DIR / "pr_curve.png", dpi=150)
    return fig


def plot_feature_importance(model, feature_names: list, top_n: int = 15,
                             save: bool = True) -> plt.Figure:
    clf = model.named_steps["clf"]
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.barh(range(top_n), importances[indices][::-1], color="steelblue")
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in indices[::-1]], fontsize=9)
    ax.set_xlabel("Importance"); ax.set_title(f"Top {top_n} Feature Importances")
    plt.tight_layout()
    if save:
        fig.savefig(REPORTS_DIR / "feature_importance.png", dpi=150)
    return fig


def plot_threshold_analysis(y_test, y_proba, save: bool = True) -> plt.Figure:
    thresholds = np.linspace(0.1, 0.9, 50)
    precisions, recalls, f1s = [], [], []
    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)
        from sklearn.metrics import precision_score, recall_score
        precisions.append(precision_score(y_test, y_pred, zero_division=0))
        recalls.append(recall_score(y_test, y_pred, zero_division=0))
        f1s.append(f1_score(y_test, y_pred, zero_division=0))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(thresholds, precisions, label="Precision")
    ax.plot(thresholds, recalls,   label="Recall")
    ax.plot(thresholds, f1s,       label="F1", lw=2)
    ax.axvline(0.5, color="k", linestyle="--", lw=1, label="Default (0.5)")
    ax.set_xlabel("Decision Threshold"); ax.set_ylabel("Score")
    ax.set_title("Metrics vs Decision Threshold")
    ax.legend(); plt.tight_layout()
    if save:
        fig.savefig(REPORTS_DIR / "threshold_analysis.png", dpi=150)
    return fig
