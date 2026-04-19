"""Load saved model and make price predictions."""

import pathlib
import pandas as pd
import joblib

MODELS_DIR  = pathlib.Path(__file__).parent / "models"
MODEL_PATH  = MODELS_DIR / "house_model.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
META_PATH   = MODELS_DIR / "meta.joblib"


def _check_models() -> None:
    for p in (MODEL_PATH, SCALER_PATH, META_PATH):
        if not p.exists():
            raise FileNotFoundError(
                f"Model file not found: {p}\n"
                "Run  python train.py  first."
            )


def predict_price(features: dict) -> float:
    """Return predicted house price in USD for a feature dict."""
    _check_models()
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    meta   = joblib.load(META_PATH)

    X = pd.DataFrame([features])[meta["features"]]
    X_s = scaler.transform(X)
    return float(model.predict(X_s)[0])


def load_meta() -> dict:
    """Return model metadata (metrics, feature names, importances)."""
    _check_models()
    return joblib.load(META_PATH)


if __name__ == "__main__":
    sample = {
        "MedInc": 5.0, "HouseAge": 20.0, "AveRooms": 6.0,
        "AveBedrms": 1.0, "Population": 1000.0, "AveOccup": 3.0,
        "Latitude": 34.0, "Longitude": -118.0,
    }
    price = predict_price(sample)
    print(f"Predicted price: ${price:,.0f}")
