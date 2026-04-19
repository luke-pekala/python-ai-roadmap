import pandas as pd
import pytest
from features import engineer_features, extract_title, NUMERIC_COLS, CATEGORICAL_COLS


def make_row(**kwargs):
    defaults = dict(
        PassengerId=1, Survived=1, Pclass=3, Name="Smith, Mr. John",
        Sex="male", Age=30.0, SibSp=1, Parch=0, Ticket="A123",
        Fare=7.25, Cabin=None, Embarked="S",
    )
    defaults.update(kwargs)
    return pd.DataFrame([defaults])


def test_extract_title_mr():
    assert extract_title("Smith, Mr. John") == "Mr"


def test_extract_title_rare():
    assert extract_title("Smith, Dr. John") == "Rare"


def test_extract_title_mlle_mapped():
    assert extract_title("Dupont, Mlle. Anne") == "Miss"


def test_family_size_solo():
    df = engineer_features(make_row(SibSp=0, Parch=0))
    assert df["family_size"].iloc[0] == 1
    assert df["is_alone"].iloc[0] == 1


def test_family_size_group():
    df = engineer_features(make_row(SibSp=2, Parch=1))
    assert df["family_size"].iloc[0] == 4
    assert df["is_alone"].iloc[0] == 0


def test_cabin_known_true():
    df = engineer_features(make_row(Cabin="C123"))
    assert df["cabin_known"].iloc[0] == 1


def test_cabin_known_false():
    df = engineer_features(make_row(Cabin=None))
    assert df["cabin_known"].iloc[0] == 0


def test_fare_per_person():
    df = engineer_features(make_row(Fare=30.0, SibSp=2, Parch=0))
    assert abs(df["fare_per_person"].iloc[0] - 10.0) < 0.01


def test_deck_extracted():
    df = engineer_features(make_row(Cabin="B77"))
    assert df["deck"].iloc[0] == "B"


def test_deck_unknown():
    df = engineer_features(make_row(Cabin=None))
    assert df["deck"].iloc[0] == "U"


def test_ticket_prefix_extracted():
    df = engineer_features(make_row(Ticket="PC 17599"))
    assert df["ticket_prefix"].iloc[0] == "PC"


def test_ticket_prefix_numeric_becomes_none():
    df = engineer_features(make_row(Ticket="12345"))
    assert df["ticket_prefix"].iloc[0] == "NONE"


def test_numeric_cols_present():
    df = engineer_features(make_row())
    for col in NUMERIC_COLS:
        assert col in df.columns, f"{col} missing"


def test_categorical_cols_present():
    df = engineer_features(make_row())
    for col in CATEGORICAL_COLS:
        assert col in df.columns, f"{col} missing"
