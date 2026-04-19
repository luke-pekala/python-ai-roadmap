"""Module I — House Price Predictor (Streamlit app)."""

import pathlib
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

MODELS_DIR = pathlib.Path(__file__).parent / "models"


def _ensure_model() -> None:
    """Auto-train if model files are missing."""
    if not (MODELS_DIR / "house_model.joblib").exists():
        with st.spinner("Training model for the first time — ~20 seconds…"):
            subprocess.run(
                [sys.executable, str(pathlib.Path(__file__).parent / "train.py")],
                check=True,
            )


def main() -> None:
    st.set_page_config(
        page_title="House Price Predictor · Module I",
        page_icon="🏠",
        layout="wide",
    )

    _ensure_model()

    from predict import load_meta, predict_price  # noqa: PLC0415

    meta = load_meta()

    # ── Header ────────────────────────────────────────────────────────────────
    st.title("🏠 House Price Predictor")
    st.caption(
        f"RandomForestRegressor · R² = **{meta['r2']:.3f}** · "
        f"MAE = **${meta['mae']:,.0f}**"
    )

    # ── Two-column layout ─────────────────────────────────────────────────────
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.subheader("Enter house features")

        med_inc   = st.slider("Median income (×$10k)",      0.5, 15.0, 5.0,  0.1)
        house_age = st.slider("House age (years)",           1,   52,   20)
        ave_rooms = st.slider("Average rooms per household", 1.0, 15.0,  6.0, 0.5)
        ave_beds  = st.slider("Average bedrooms",            1.0,  5.0,  1.0, 0.1)
        population= st.slider("Block population",            3,  35000, 1000, 10)
        ave_occup = st.slider("Average occupants",           1.0, 10.0,  3.0, 0.1)
        latitude  = st.slider("Latitude",                   32.5, 42.0, 34.0, 0.1)
        longitude = st.slider("Longitude",                 -124.0,-114.0,-118.0,0.1)

        features = {
            "MedInc":     med_inc,
            "HouseAge":   float(house_age),
            "AveRooms":   ave_rooms,
            "AveBedrms":  ave_beds,
            "Population": float(population),
            "AveOccup":   ave_occup,
            "Latitude":   latitude,
            "Longitude":  longitude,
        }

        price = predict_price(features)
        st.metric("Predicted price", f"${price:,.0f}")

    with right:
        st.subheader("Feature importance")
        fi_df = pd.DataFrame({
            "Feature":   meta["features"],
            "Importance": meta["feature_importances"],
        }).sort_values("Importance", ascending=True)

        fig = px.bar(
            fi_df,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Blues",
            template="plotly_dark",
        )
        fig.update_layout(
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Model metrics")
        c1, c2 = st.columns(2)
        c1.metric("R² score",  f"{meta['r2']:.3f}", help="1.0 = perfect. >0.8 = good.")
        c2.metric("MAE",       f"${meta['mae']:,.0f}", help="Average prediction error.")

    # ── About ─────────────────────────────────────────────────────────────────
    with st.expander("About this app"):
        st.markdown(
            """
**Dataset**: California Housing (scikit-learn built-in, ~20 000 rows)

**Model**: `RandomForestRegressor(n_estimators=100)`

**Pipeline**: fetch → train/test split (80/20) → StandardScaler → fit → joblib save

**R² explained**: 0.85 means the model explains 85 % of the variance in house prices.
An R² above 0.80 is considered good for a housing regression task.

**Feature importance**: shows which inputs drive predictions most.
Median income and location (lat/lon) dominate for California housing.
            """
        )


if __name__ == "__main__":
    main()
