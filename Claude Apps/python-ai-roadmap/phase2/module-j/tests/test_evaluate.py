import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from evaluate import (
    get_metrics, plot_confusion_matrix, plot_roc_curve,
    plot_pr_curve, plot_feature_importance, plot_threshold_analysis,
)


@pytest.fixture(scope="module")
def dummy_model():
    rng = np.random.default_rng(42)
    X = pd.DataFrame(rng.standard_normal((300, 5)),
                     columns=[f"f{i}" for i in range(5)])
    y = pd.Series((X["f0"] + X["f1"] > 0).astype(int))
    pipe = Pipeline([("scaler", StandardScaler()),
                     ("clf", RandomForestClassifier(n_estimators=20, random_state=42))])
    pipe.fit(X, y)
    return pipe, X, y


def test_metrics_keys(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    for key in ("f1", "roc_auc", "avg_precision", "report", "cm", "y_pred", "y_proba"):
        assert key in m, f"Missing key: {key}"


def test_metrics_ranges(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert 0.0 <= m["f1"]            <= 1.0
    assert 0.0 <= m["roc_auc"]       <= 1.0
    assert 0.0 <= m["avg_precision"] <= 1.0


def test_confusion_matrix_shape(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert m["cm"].shape == (2, 2)


def test_y_proba_range(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert m["y_proba"].min() >= 0.0
    assert m["y_proba"].max() <= 1.0


def test_y_pred_binary(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert set(np.unique(m["y_pred"])).issubset({0, 1})


def test_plot_confusion_matrix_returns_figure(dummy_model):
    import matplotlib.pyplot as plt
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    fig = plot_confusion_matrix(m["cm"], save=False)
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_plot_roc_curve_returns_figure(dummy_model):
    import matplotlib.pyplot as plt
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    fig = plot_roc_curve(y, m["y_proba"], m["roc_auc"], save=False)
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_plot_pr_curve_returns_figure(dummy_model):
    import matplotlib.pyplot as plt
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    fig = plot_pr_curve(y, m["y_proba"], m["avg_precision"], save=False)
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_plot_feature_importance_returns_figure(dummy_model):
    import matplotlib.pyplot as plt
    model, X, y = dummy_model
    feature_names = list(X.columns)
    fig = plot_feature_importance(model, feature_names, top_n=5, save=False)
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_plot_threshold_analysis_returns_figure(dummy_model):
    import matplotlib.pyplot as plt
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    fig = plot_threshold_analysis(y, m["y_proba"], save=False)
    assert hasattr(fig, "savefig")
    plt.close(fig)


def test_classification_report_has_classes(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert "0" in m["report"] or 0 in m["report"]


def test_high_threshold_flags_few(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    flagged = (m["y_proba"] >= 0.9).sum()
    assert flagged < len(y)


def test_low_threshold_flags_many(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    flagged = (m["y_proba"] >= 0.1).sum()
    assert flagged > 0


def test_roc_auc_better_than_random(dummy_model):
    model, X, y = dummy_model
    m = get_metrics(model, X, y)
    assert m["roc_auc"] > 0.5
