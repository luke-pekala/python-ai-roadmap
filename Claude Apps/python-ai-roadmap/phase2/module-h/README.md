# Module H — Interactive Visualisation

**Phase 2 · Weeks 11–12 · Python AI Roadmap**

An interactive data explorer built with Streamlit and Plotly.  
Upload any CSV, pick columns, and render bar, line, histogram, or scatter charts — all in the browser with zero frontend code.

## Stack
| Tool | Purpose |
|------|---------|
| Streamlit | Web UI from pure Python |
| Plotly Express | Interactive browser charts |
| Pandas | DataFrame handling |
| statsmodels | OLS trendline for scatter |

## Run locally

```bash
cd phase2/module-h
uv sync
.venv\Scripts\streamlit.exe run app.py          # Windows
# or
uv run streamlit run app.py                      # Mac / Linux
```

Open http://localhost:8501 — upload a CSV or click **Load sample sales data**.

## Tests

```bash
uv run pytest
```

20 tests · 100% coverage on `charts.py`.

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub
2. Go to https://share.streamlit.io → **New app**
3. Set **Main file path** to `phase2/module-h/app.py`
4. Click **Deploy** — live URL in ~1 minute

## Project structure

```
module-h/
├── app.py              # Streamlit app (UI layer)
├── charts.py           # Chart functions (pure, testable)
├── tests/
│   └── test_charts.py
├── pyproject.toml
└── README.md
```
