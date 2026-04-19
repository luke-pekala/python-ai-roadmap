"""Tests for DigitNet model — no training required."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
import torch

from model import DigitNet


# ── architecture tests ────────────────────────────────────────────────────────

def test_output_shape_single():
    model = DigitNet()
    x = torch.randn(1, 1, 28, 28)
    out = model(x)
    assert out.shape == (1, 10), f"Expected (1,10), got {out.shape}"


def test_output_shape_batch():
    model = DigitNet()
    x = torch.randn(64, 1, 28, 28)
    out = model(x)
    assert out.shape == (64, 10)


def test_output_is_logits_not_probabilities():
    """Raw output should NOT sum to 1 (that would mean softmax was applied)."""
    model = DigitNet()
    x = torch.randn(4, 1, 28, 28)
    out = model(x)
    sums = out.sum(dim=1)
    assert not torch.allclose(sums, torch.ones(4), atol=0.1),         "Output looks like probabilities — remove softmax from forward()"


def test_parameter_count():
    """Sanity check that the network has parameters."""
    model = DigitNet()
    total = sum(p.numel() for p in model.parameters())
    assert total > 100_000, f"Too few parameters: {total}"


def test_different_inputs_give_different_outputs():
    model = DigitNet()
    model.eval()
    x1 = torch.randn(1, 1, 28, 28)
    x2 = torch.randn(1, 1, 28, 28)
    with torch.no_grad():
        o1 = model(x1)
        o2 = model(x2)
    assert not torch.allclose(o1, o2), "Two different inputs gave identical outputs"


def test_eval_mode_disables_dropout():
    """In eval mode, the same input should always give the same output."""
    model = DigitNet()
    model.eval()
    x = torch.randn(1, 1, 28, 28)
    with torch.no_grad():
        o1 = model(x)
        o2 = model(x)
    assert torch.allclose(o1, o2)


def test_argmax_returns_valid_class():
    model = DigitNet()
    model.eval()
    x = torch.randn(10, 1, 28, 28)
    with torch.no_grad():
        preds = model(x).argmax(dim=1)
    assert preds.min() >= 0
    assert preds.max() <= 9


# ── predict() function tests ──────────────────────────────────────────────────

def _make_fake_model(tmp_path):
    """Save a freshly-initialised (untrained) model to a temp path."""
    m = DigitNet()
    save = tmp_path / "mnist.pth"
    torch.save(m.state_dict(), save)
    return save


def test_predict_returns_int(tmp_path, monkeypatch):
    save = _make_fake_model(tmp_path)
    monkeypatch.setattr("predict.MODEL_PATH", save)
    import predict as P
    P._model = None                                    # reset cached model
    img = np.zeros((28, 28), dtype=np.uint8)
    img[10:18, 10:18] = 200                            # a white square
    result = P.predict(img)
    assert isinstance(result, int)
    assert 0 <= result <= 9


def test_predict_range(tmp_path, monkeypatch):
    save = _make_fake_model(tmp_path)
    monkeypatch.setattr("predict.MODEL_PATH", save)
    import predict as P
    P._model = None
    for _ in range(10):
        img = np.random.randint(0, 256, (28, 28), dtype=np.uint8)
        assert 0 <= P.predict(img) <= 9


def test_predict_blank_canvas(tmp_path, monkeypatch):
    """All-black image should still return a valid class (model doesn't crash)."""
    save = _make_fake_model(tmp_path)
    monkeypatch.setattr("predict.MODEL_PATH", save)
    import predict as P
    P._model = None
    img = np.zeros((28, 28), dtype=np.uint8)
    result = P.predict(img)
    assert 0 <= result <= 9
