# Module J — Model Evaluation

**Telco Customer Churn Classifier with Full Evaluation Suite**

## What it does
- Downloads Telco Churn dataset (~7 000 rows) and trains a Random Forest
- 5-fold stratified cross-validation (F1 + ROC-AUC)
- Interactive Streamlit dashboard: confusion matrix, ROC curve, PR curve,
  feature importance, threshold analysis, live threshold tuner

## Quick start
```bash
uv venv --python 3.12
uv sync --all-groups
streamlit run app.py
```

## Run tests
```bash
uv run pytest
```

## Key metrics (typical)
| Metric | Value |
|--------|-------|
| CV F1  | ~0.62 |
| CV ROC-AUC | ~0.85 |
| Test ROC-AUC | ~0.86 |
