# Module Y — Autonomous Research Crew

Multi-agent system: four specialised Claude agents orchestrated to produce
a verified research report from a single question.

## Agents
| Agent | Role |
|-------|------|
| Searcher | Gathers background knowledge |
| Analyst | Extracts insights + confidence ratings |
| Writer | Drafts the structured report |
| Checker | Fact-checks and annotates |

## Setup
```
uv venv --python 3.12
uv sync --all-groups
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## Run
```
uv run pytest            # 14 tests, no API calls
uv run streamlit run app.py
```
