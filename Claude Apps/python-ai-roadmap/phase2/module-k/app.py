"""Streamlit dashboard — Titanic Feature Engineering & ML Pipeline (Module K)."""
import io
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.inspection import permutation_importance
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from features import DROP_COLS, engineer_features
from pipeline import full_pipeline
from train import DATA_DIR, MODEL_PATH, load_data, train

st.set_page_config(page_title="Module K — Titanic Pipeline", layout="wide")
st.title("Module K · Titanic Feature Engineering Pipeline")
st.caption("Weeks 17-18 · sklearn Pipeline · ColumnTransformer · Feature Engineering")

# ── Sidebar: data source ──────────────────────────────────────────────────
st.sidebar.header("Data Source")
uploaded = st.sidebar.file_uploader(
    "Upload your own train CSV (optional)", type="csv",
    help="Must include a 'Survived' column and the standard Titanic columns."
)

@st.cache_data(show_spinner="Loading data...")
def get_data(file_bytes: bytes | None) -> pd.DataFrame:
    if file_bytes:
        raw = pd.read_csv(io.BytesIO(file_bytes))
    else:
        path = DATA_DIR / "train.csv"
        if not path.exists():
            st.error(
                "data/train.csv not found.\n\n"
                "Download from https://www.kaggle.com/c/titanic and place in the data/ folder."
            )
            st.stop()
        raw = pd.read_csv(path)
    df = engineer_features(raw)
    return df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")

file_bytes = uploaded.read() if uploaded else None
df = get_data(file_bytes)
X = df.drop(columns=["Survived"])
y = df["Survived"]

# ── Train / load model ────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Training pipeline...")
def get_model(cache_key: str):
    if MODEL_PATH.exists() and not uploaded:
        return joblib.load(MODEL_PATH)
    result = train()
    return joblib.load(MODEL_PATH), result

model = get_model("uploaded" if uploaded else "default")
if isinstance(model, tuple):
    model, _ = model

# ── CV score ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Running cross-validation...")
def get_cv(cache_key: str):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(full_pipeline, X, y, cv=cv, scoring="accuracy")
    return scores

cv_scores = get_cv("uploaded" if uploaded else "default")

# ── Top metrics ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("CV Accuracy (mean)", f"{cv_scores.mean():.3f}")
c2.metric("CV Std", f"{cv_scores.std():.3f}")
c3.metric("Passengers (train)", len(df))
c4.metric("Survival rate", f"{y.mean():.1%}")

st.divider()

# ── Feature importance tab + engineered features tab ─────────────────────
tab1, tab2, tab3 = st.tabs(["Feature Importance", "Engineered Features", "Pipeline Inspector"])

with tab1:
    st.subheader("Permutation Feature Importance")
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    fitted = full_pipeline.fit(X_tr, y_tr)

    @st.cache_data(show_spinner="Computing importances...")
    def get_importances(cache_key: str):
        result = permutation_importance(
            fitted, X_te, y_te, n_repeats=10, random_state=42, scoring="accuracy"
        )
        imp_df = pd.DataFrame({
            "feature": X_te.columns,
            "importance": result.importances_mean,
            "std": result.importances_std,
        }).sort_values("importance", ascending=False).head(15)
        return imp_df

    imp_df = get_importances("uploaded" if uploaded else "default")
    st.bar_chart(imp_df.set_index("feature")["importance"])
    st.caption("Higher = removing this feature hurts accuracy more")

with tab2:
    st.subheader("Engineered Feature Distributions")
    feat = st.selectbox(
        "Choose a feature",
        ["title", "family_size_cat", "deck", "fare_per_person", "age_bucket", "is_alone", "cabin_known"],
    )
    raw_df = pd.read_csv(DATA_DIR / "train.csv") if not uploaded else pd.read_csv(io.BytesIO(file_bytes))
    eng_df = engineer_features(raw_df)

    if feat in ["fare_per_person"]:
        col_data = eng_df[[feat, "Survived"]].dropna()
        survived = col_data[col_data["Survived"] == 1][feat].clip(upper=200)
        not_survived = col_data[col_data["Survived"] == 0][feat].clip(upper=200)
        chart_df = pd.DataFrame({"Survived": survived.reset_index(drop=True),
                                  "Not survived": not_survived.reset_index(drop=True)})
        st.line_chart(chart_df)
    else:
        counts = eng_df.groupby([feat, "Survived"]).size().unstack(fill_value=0)
        counts.columns = ["Not survived", "Survived"]
        st.bar_chart(counts)

    surv_rate = eng_df.groupby(feat)["Survived"].mean().sort_values(ascending=False)
    st.write("Survival rate by category:")
    st.dataframe(surv_rate.rename("survival_rate").reset_index(), use_container_width=True)

with tab3:
    st.subheader("Pipeline Steps")
    for i, (name, step) in enumerate(full_pipeline.steps):
        st.markdown(f"**Step {i+1}: `{name}`** — `{type(step).__name__}`")
        if hasattr(step, "transformers"):
            for tname, transformer, cols in step.transformers:
                st.markdown(f"  - `{tname}`: {type(transformer).__name__} on {cols}")
    st.info(
        "Key insight: the entire Pipeline (preprocessing + model) is fit on training data "
        "only. The same transformations are automatically applied to test data — "
        "preventing data leakage."
    )

st.divider()
st.subheader("Raw engineered dataframe (first 10 rows)")
st.dataframe(df.head(10), use_container_width=True)
