import streamlit as st
import joblib
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from train    import train, MODELS_DIR
from evaluate import (
    get_metrics, plot_confusion_matrix, plot_roc_curve,
    plot_pr_curve, plot_feature_importance, plot_threshold_analysis,
)

st.set_page_config(page_title="Module J — Churn Evaluation", layout="wide")
st.title("Module J — Model Evaluation Dashboard")
st.caption("Telco Customer Churn | Random Forest | Full Eval Suite")

# ── Load or train ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Training model (first run ~30s)...")
def load_model():
    model_path = MODELS_DIR / "churn_model.joblib"
    data_path  = MODELS_DIR / "test_data.joblib"
    feat_path  = MODELS_DIR / "feature_names.joblib"
    if not (model_path.exists() and data_path.exists()):
        train()
    model         = joblib.load(model_path)
    X_test, y_test = joblib.load(data_path)
    feature_names = joblib.load(feat_path)
    return model, X_test, y_test, feature_names

model, X_test, y_test, feature_names = load_model()
metrics = get_metrics(model, X_test, y_test)

# ── Top KPI row ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("F1 Score",       f"{metrics['f1']:.3f}")
c2.metric("ROC-AUC",        f"{metrics['roc_auc']:.3f}")
c3.metric("Avg Precision",  f"{metrics['avg_precision']:.3f}")
c4.metric("Test samples",   str(len(y_test)))

st.divider()

# ── Charts row 1 ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.subheader("Confusion Matrix")
    fig = plot_confusion_matrix(metrics["cm"], save=False)
    st.pyplot(fig); plt.close(fig)
    st.caption("Rows = actual, Columns = predicted")

with col2:
    st.subheader("ROC Curve")
    fig = plot_roc_curve(y_test, metrics["y_proba"], metrics["roc_auc"], save=False)
    st.pyplot(fig); plt.close(fig)
    st.caption("AUC of 1.0 = perfect separation, 0.5 = random")

# ── Charts row 2 ─────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    st.subheader("Precision-Recall Curve")
    fig = plot_pr_curve(y_test, metrics["y_proba"], metrics["avg_precision"], save=False)
    st.pyplot(fig); plt.close(fig)
    st.caption("Dashed baseline = churn rate in test set")

with col4:
    st.subheader("Metrics vs Decision Threshold")
    fig = plot_threshold_analysis(y_test, metrics["y_proba"], save=False)
    st.pyplot(fig); plt.close(fig)
    st.caption("Lower threshold -> more churners flagged (higher recall, lower precision)")

st.divider()

# ── Feature importance full width ─────────────────────────────────────────────
st.subheader("Top 15 Feature Importances")
fig = plot_feature_importance(model, feature_names, save=False)
st.pyplot(fig); plt.close(fig)

st.divider()

# ── Classification report table ──────────────────────────────────────────────
st.subheader("Classification Report")
report = metrics["report"]
import pandas as pd
rows = {k: v for k, v in report.items()
        if k not in ("accuracy", "macro avg", "weighted avg")}
df_report = pd.DataFrame(rows).T.round(3)
st.dataframe(df_report, use_container_width=True)

# ── Threshold slider ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Live Threshold Tuner")
threshold = st.slider("Decision threshold", 0.1, 0.9, 0.5, 0.01)
y_pred_t = (metrics["y_proba"] >= threshold).astype(int)
from sklearn.metrics import precision_score, recall_score, f1_score as f1s
p = precision_score(y_test, y_pred_t, zero_division=0)
r = recall_score(y_test, y_pred_t, zero_division=0)
f = f1s(y_test, y_pred_t, zero_division=0)
flagged = int(y_pred_t.sum())
tc1, tc2, tc3, tc4 = st.columns(4)
tc1.metric("Precision", f"{p:.3f}")
tc2.metric("Recall",    f"{r:.3f}")
tc3.metric("F1",        f"{f:.3f}")
tc4.metric("Customers flagged", str(flagged))
st.caption("Move the threshold left to catch more churners (raises recall). "
           "Move it right to reduce false alarms (raises precision).")
