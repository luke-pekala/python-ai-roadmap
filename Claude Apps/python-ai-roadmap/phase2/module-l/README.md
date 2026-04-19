# Module L — Neural Net Basics · MNIST Digit Classifier

Phase 2 · Weeks 19–20  
**Tech:** PyTorch · torchvision · Streamlit · pytest

## What it does
Trains a 3-layer MLP on MNIST (60 000 handwritten digits).  
Streamlit app lets you **draw a digit** and get a real-time prediction with a confidence bar chart.

## Quick start

```bash
uv venv --python 3.12
uv sync --all-groups
uv run python train.py        # ~2 min CPU, downloads MNIST automatically
uv run pytest                 # 10 tests — all should pass
uv run streamlit run app.py   # open http://localhost:8501
```

## Expected accuracy
≥ 98 % on the MNIST test set after 10 epochs.

## Project structure
```
module-l/
├── model.py          # DigitNet architecture
├── train.py          # training loop + save weights
├── predict.py        # load model + predict single image
├── app.py            # Streamlit draw-and-predict UI
├── models/           # mnist.pth saved here after training
├── data/             # MNIST downloaded here automatically
├── tests/
│   └── test_model.py
└── README.md
```

## Key concepts covered
- Tensors and nn.Module
- Forward pass, loss (CrossEntropyLoss), backpropagation
- Adam optimizer, Dropout regularisation
- Saving/loading state_dict
- Real-time inference in a Streamlit UI
