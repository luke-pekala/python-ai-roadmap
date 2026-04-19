"""Tests for Module M — all mocked, no real API calls."""
import json
import pytest
from unittest.mock import MagicMock, patch


MOCK_RESPONSE = {
    "summary": "A short summary of the test text.",
    "key_points": ["Point A", "Point B"],
    "action_items": ["Do X", "Review Y"],
    "tldr": "Very short.",
}


def make_mock_message():
    msg = MagicMock()
    msg.content = [MagicMock(text=json.dumps(MOCK_RESPONSE))]
    return msg


# ── client.summarise ──────────────────────────────────────────────────────

@patch("client.get_client")
def test_summarise_returns_dict(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert isinstance(result, dict)


@patch("client.get_client")
def test_summarise_has_required_keys(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert "summary" in result
    assert "key_points" in result
    assert "action_items" in result
    assert "tldr" in result


@patch("client.get_client")
def test_key_points_is_list(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert isinstance(result["key_points"], list)


@patch("client.get_client")
def test_action_items_is_list(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert isinstance(result["action_items"], list)


@patch("client.get_client")
def test_tldr_is_string(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert isinstance(result["tldr"], str)


@patch("client.get_client")
def test_summary_is_string(mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = make_mock_message()
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some test text")
    assert isinstance(result["summary"], str)


# ── JSON parse fallback ───────────────────────────────────────────────────

@patch("client.get_client")
def test_invalid_json_fallback(mock_get_client):
    """If Claude returns non-JSON, we get a safe fallback dict."""
    msg = MagicMock()
    msg.content = [MagicMock(text="Sorry, I cannot summarise that.")]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = msg
    mock_get_client.return_value = mock_client

    from client import summarise
    result = summarise("Some text")
    assert isinstance(result, dict)
    assert "summary" in result


# ── get_client ────────────────────────────────────────────────────────────

def test_get_client_raises_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    import importlib, client
    importlib.reload(client)
    with pytest.raises(EnvironmentError):
        client.get_client()


# ── prompts ───────────────────────────────────────────────────────────────

def test_build_user_prompt_contains_text():
    from prompts import build_user_prompt
    prompt = build_user_prompt("hello world")
    assert "hello world" in prompt


def test_system_json_prompt_contains_schema():
    from prompts import SYSTEM_JSON
    assert "key_points" in SYSTEM_JSON
    assert "action_items" in SYSTEM_JSON
    assert "tldr" in SYSTEM_JSON


def test_system_plain_prompt_exists():
    from prompts import SYSTEM_PLAIN
    assert len(SYSTEM_PLAIN) > 10


# ── summariser CLI helpers ────────────────────────────────────────────────

def test_render_plain(capsys):
    from summariser import render
    result = {
        "summary": "Test summary",
        "key_points": ["A", "B"],
        "action_items": ["Do this"],
        "tldr": "Short.",
    }
    render(result, "plain")
    captured = capsys.readouterr()
    assert "Test summary" in captured.out
    assert "Short." in captured.out


def test_render_json(capsys):
    from summariser import render
    result = {
        "summary": "Test",
        "key_points": [],
        "action_items": [],
        "tldr": "TL;DR",
    }
    render(result, "json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["summary"] == "Test"


def test_render_markdown(capsys):
    from summariser import render
    result = {
        "summary": "Markdown summary",
        "key_points": ["Point 1"],
        "action_items": [],
        "tldr": "Short.",
    }
    render(result, "markdown")
    captured = capsys.readouterr()
    assert "## Summary" in captured.out
    assert "Point 1" in captured.out
