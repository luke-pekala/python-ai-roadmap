"""Feature engineering for the Titanic dataset."""
import re
import pandas as pd

TITLE_MAP = {
    "Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs",
    "Lady": "Rare", "Countess": "Rare", "Capt": "Rare",
    "Col": "Rare", "Don": "Rare", "Dr": "Rare",
    "Major": "Rare", "Rev": "Rare", "Sir": "Rare",
    "Jonkheer": "Rare", "Dona": "Rare",
}


def extract_title(name: str) -> str:
    match = re.search(r" ([A-Za-z]+)\.", name)
    title = match.group(1) if match else "Unknown"
    return TITLE_MAP.get(title, title)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns to a raw Titanic dataframe."""
    df = df.copy()

    # Family
    df["family_size"] = df["SibSp"] + df["Parch"] + 1
    df["is_alone"] = (df["family_size"] == 1).astype(int)
    df["family_size_cat"] = pd.cut(
        df["family_size"],
        bins=[0, 1, 4, 20],
        labels=["alone", "small", "large"],
    )

    # Title from name
    df["title"] = df["Name"].apply(extract_title)

    # Cabin info
    df["cabin_known"] = df["Cabin"].notna().astype(int)
    df["deck"] = df["Cabin"].str[0].fillna("U")

    # Fare per person (avoid zero-division)
    df["fare_per_person"] = df["Fare"] / df["family_size"].clip(lower=1)

    # Ticket prefix
    df["ticket_prefix"] = df["Ticket"].str.replace(r"[^A-Za-z]", "", regex=True)
    df["ticket_prefix"] = df["ticket_prefix"].where(df["ticket_prefix"] != "", "NONE")

    # Age buckets (before imputation fills NaN)
    df["age_bucket"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 120],
        labels=["child", "teen", "adult", "middle", "senior"],
    )

    return df


NUMERIC_COLS = ["Age", "Fare", "SibSp", "Parch", "family_size", "fare_per_person"]
CATEGORICAL_COLS = [
    "Pclass", "Sex", "Embarked", "title",
    "family_size_cat", "deck", "ticket_prefix", "age_bucket",
]
DROP_COLS = ["PassengerId", "Name", "Ticket", "Cabin"]
