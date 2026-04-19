# Module K — Feature Engineering

**Weeks 17–18 | Phase 2: Data, ML and Model Basics**

Titanic survival prediction with a full `sklearn` Pipeline:
custom feature engineering, `ColumnTransformer`, `GradientBoostingClassifier`,
cross-validation, and a Streamlit dashboard.

## Quick start

```bash
uv venv --python 3.12
uv sync --all-groups
# Place train.csv (and optionally test.csv) in data/
uv run python train.py      # trains + saves model
uv run pytest               # 14 tests
uv run streamlit run app.py # dashboard
```

## Dataset

Download `train.csv` and `test.csv` from
<https://www.kaggle.com/c/titanic/data> and place them in `data/`.

## Kaggle submission

```bash
uv run python train.py      # generates submission.csv
# Upload submission.csv at kaggle.com/c/titanic
```

Expected CV accuracy: ~0.83

## Skills covered

- Feature engineering (title, family size, deck, fare per person)
- `sklearn` Pipeline + `ColumnTransformer`
- `SimpleImputer`, `OneHotEncoder`, `StandardScaler`
- Data leakage prevention
- Permutation feature importance
- Kaggle submission workflow
