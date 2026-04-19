"""Tests for Module I — predict.py"""

import pathlib
import subprocess
import sys

import pytest

MODELS_DIR = pathlib.Path(__file__).parent.parent / "models"

SAMPLE = {
    "MedInc": 5.0, "HouseAge": 20.0, "AveRooms": 6.0,
    "AveBedrms": 1.0, "Population": 1000.0, "AveOccup": 3.0,
    "Latitude": 34.0, "Longitude": -118.0,
}


@pytest.fixture(scope="session", autouse=True)
def trained_model():
    """Ensure model is trained before any test runs."""
    train_script = pathlib.Path(__file__).parent.parent / "train.py"
    subprocess.run([sys.executable, str(train_script)], check=True)


class TestPredictPrice:
    def test_returns_positive_float(self):
        from predict import predict_price
        price = predict_price(SAMPLE)
        assert isinstance(price, float)
        assert price > 0

    def test_price_in_plausible_range(self):
        from predict import predict_price
        price = predict_price(SAMPLE)
        assert 10_000 < price < 5_000_000

    def test_higher_income_raises_price(self):
        from predict import predict_price
        low  = predict_price({**SAMPLE, "MedInc": 1.0})
        high = predict_price({**SAMPLE, "MedInc": 12.0})
        assert high > low

    def test_different_features_differ(self):
        from predict import predict_price
        p1 = predict_price(SAMPLE)
        p2 = predict_price({**SAMPLE, "HouseAge": 50.0, "AveRooms": 2.0})
        assert p1 != p2


class TestLoadMeta:
    def test_meta_has_required_keys(self):
        from predict import load_meta
        meta = load_meta()
        for key in ("mae", "r2", "features", "feature_importances"):
            assert key in meta

    def test_r2_is_reasonable(self):
        from predict import load_meta
        meta = load_meta()
        assert 0.5 < meta["r2"] < 1.0

    def test_mae_positive(self):
        from predict import load_meta
        meta = load_meta()
        assert meta["mae"] > 0

    def test_features_list_length(self):
        from predict import load_meta
        meta = load_meta()
        assert len(meta["features"]) == 8

    def test_importances_sum_to_one(self):
        from predict import load_meta
        meta = load_meta()
        total = sum(meta["feature_importances"])
        assert abs(total - 1.0) < 1e-6


class TestModelFiles:
    def test_model_file_exists(self):
        assert (MODELS_DIR / "house_model.joblib").exists()

    def test_scaler_file_exists(self):
        assert (MODELS_DIR / "scaler.joblib").exists()

    def test_meta_file_exists(self):
        assert (MODELS_DIR / "meta.joblib").exists()
