# Module M — Smart Summariser CLI
**Phase 3 · Week 21–22 · Anthropic API**

A CLI tool that reads any text file, URL, or raw text, sends it to Claude with a
structured prompt, and returns a clean summary with key points, action items, and
a one-sentence TL;DR. Supports plain, markdown, and JSON output formats.

## Setup
```bash
uv venv --python 3.12
uv sync --all-groups
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage — CLI
```bash
uv run python summariser.py --file myfile.txt
uv run python summariser.py --url https://example.com/article
uv run python summariser.py --text "Paste any text here"
uv run python summariser.py --file myfile.txt --format json
uv run python summariser.py --file myfile.txt --format markdown
uv run python summariser.py --file myfile.txt --stream
```

## Usage — Streamlit dashboard
```bash
uv run streamlit run app.py
```

## Tests
```bash
uv run pytest
```
All tests are mocked — no real API calls needed.

## Skills covered
- Anthropic SDK setup and auth
- `messages.create()` with system prompts
- Structured JSON output from Claude
- Streaming with `messages.stream()`
- API key management via `.env`
- Mock testing with `unittest.mock`
