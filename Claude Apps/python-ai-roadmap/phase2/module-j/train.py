import os, joblib, warnings
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore")

DATA_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)
MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def load_data() -> pd.DataFrame:
    cache = MODELS_DIR / "churn_data.csv"
    if cache.exists():
        return pd.read_csv(cache)
    print("Downloading Telco Churn dataset...")
    df = pd.read_csv(DATA_URL)
    df.to_csv(cache, index=False)
    return df


def preprocess(df: pd.DataFrame):
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.dropna(inplace=True)
    df.drop(columns=["customerID"], inplace=True)

    # Encode target
    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    # Encode all object columns
    le = LabelEncoder()
    for col in df.select_dtypes("object").columns:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    return X, y


def train():
    df = load_data()
    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=200, max_depth=10,
            class_weight="balanced", random_state=42, n_jobs=-1
        )),
    ])

    print("Running 5-fold stratified cross-validation...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    f1_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1")
    roc_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
    print(f"  CV F1:      {f1_scores.mean():.3f} +/- {f1_scores.std():.3f}")
    print(f"  CV ROC-AUC: {roc_scores.mean():.3f} +/- {roc_scores.std():.3f}")

    print("Fitting final model on full training set...")
    pipe.fit(X_train, y_train)

    joblib.dump(pipe,   MODELS_DIR / "churn_model.joblib")
    joblib.dump((X_test, y_test), MODELS_DIR / "test_data.joblib")
    joblib.dump(list(X.columns),  MODELS_DIR / "feature_names.joblib")
    print("Models saved to models/")
    return pipe, X_test, y_test, list(X.columns)


if __name__ == "__main__":
    train()
