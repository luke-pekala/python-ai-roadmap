"""Train the Titanic pipeline and generate submission.csv."""
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold

from features import DROP_COLS, engineer_features
from pipeline import full_pipeline

DATA_DIR = Path(__file__).parent / "data"
MODEL_PATH = Path(__file__).parent / "titanic_pipeline.joblib"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = engineer_features(df)
    return df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")


def train(train_path: Path = DATA_DIR / "train.csv") -> dict:
    df = load_data(train_path)
    X = df.drop(columns=["Survived"])
    y = df["Survived"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(full_pipeline, X, y, cv=cv, scoring="accuracy")
    print(f"CV accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

    full_pipeline.fit(X, y)
    joblib.dump(full_pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return {"cv_mean": float(scores.mean()), "cv_std": float(scores.std())}


def predict(test_path: Path = DATA_DIR / "test.csv") -> Path:
    model = joblib.load(MODEL_PATH)
    raw = pd.read_csv(test_path)
    passenger_ids = raw["PassengerId"]
    df = engineer_features(raw)
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")
    preds = model.predict(df)
    out = Path(__file__).parent / "submission.csv"
    pd.DataFrame({"PassengerId": passenger_ids, "Survived": preds}).to_csv(out, index=False)
    print(f"Submission saved to {out}")
    return out


if __name__ == "__main__":
    train()
    if (DATA_DIR / "test.csv").exists():
        predict()
    else:
        print("No test.csv found — skipping submission generation.")
