"""Train a RandomForestRegressor on California housing data and save to disk."""

import pathlib
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

MODELS_DIR = pathlib.Path(__file__).parent / "models"
MODEL_PATH  = MODELS_DIR / "house_model.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
META_PATH   = MODELS_DIR / "meta.joblib"


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load California housing dataset as a DataFrame."""
    dataset = fetch_california_housing(as_frame=True)
    X: pd.DataFrame = dataset.frame.drop(columns=["MedHouseVal"])
    y: pd.Series     = dataset.frame["MedHouseVal"] * 100_000  # scale to USD
    return X, y


def train(X: pd.DataFrame, y: pd.Series) -> dict:
    """Train model, return metrics dict."""
    MODELS_DIR.mkdir(exist_ok=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_s, y_train)

    preds = model.predict(X_test_s)
    metrics = {
        "mae":  float(mean_absolute_error(y_test, preds)),
        "r2":   float(r2_score(y_test, preds)),
        "features": list(X.columns),
        "feature_importances": model.feature_importances_.tolist(),
    }

    joblib.dump(model,  MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(metrics, META_PATH)

    print(f"MAE : ${metrics['mae']:,.0f}")
    print(f"R²  : {metrics['r2']:.3f}")
    print("Model saved →", MODEL_PATH)
    return metrics


if __name__ == "__main__":
    X, y = load_data()
    train(X, y)
