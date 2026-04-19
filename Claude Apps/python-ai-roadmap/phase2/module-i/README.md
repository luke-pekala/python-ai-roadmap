# Module I — Classic ML: House Price Predictor

> Phase 2 · Weeks 13–14 · Python AI Roadmap

A Streamlit app that trains a **RandomForestRegressor** on California housing data
and lets users predict house prices by adjusting input sliders.

## Live demo
<!-- Replace with your Streamlit Cloud URL after deploy -->
🔗 [your-app.streamlit.app](https://share.streamlit.io)

## Model performance
| Metric | Value |
|--------|-------|
| R²     | ~0.81 |
| MAE    | ~$33 000 |

## Quick start

```bash
uv venv --python 3.12
uv sync --all-groups
python train.py          # trains model, saves to models/
streamlit run app.py     # opens http://localhost:8501
```

## Run tests

```bash
uv run pytest
```

## Project layout

```
module-i/
├── train.py          # fetch data, train, save model
├── predict.py        # load model, make predictions
├── app.py            # Streamlit UI
├── models/           # saved model files (git-ignored)
├── tests/
│   └── test_predict.py
└── pyproject.toml
```

## What you learn

- **scikit-learn** fit/predict/score API — works the same for every algorithm
- **Train/test split** — why 80/20 and random_state=42
- **RandomForestRegressor** — ensemble trees, handles non-linearity
- **joblib** — save and reload trained models
- **MAE vs R²** — when to use each metric
- **Feature importance** — which inputs drive predictions most

## Skills
`scikit-learn` · `RandomForest` · `train_test_split` · `MAE + R²` · `joblib` · End-to-end ML pipeline
