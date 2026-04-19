"""Streamlit draw-and-predict app for MNIST digit classifier."""
import pathlib
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps

MODEL_PATH = pathlib.Path(__file__).parent / "models" / "mnist.pth"

st.set_page_config(page_title="Digit Classifier · Module L", page_icon="✏️", layout="centered")
st.title("✏️ Digit Classifier — Module L")
st.markdown("Draw a digit (0–9) in the box below and the neural network predicts it in real time.")

# ── sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About")
    st.markdown(
        """
**Model:** DigitNet (3-layer MLP)  
**Dataset:** MNIST (60k train / 10k test)  
**Target accuracy:** ≥ 98 %  

**Architecture**
- Flatten 28×28 → 784
- Linear 784 → 256 + ReLU + Dropout 0.2
- Linear 256 → 128 + ReLU
- Linear 128 → 10
        """
    )
    st.markdown("---")
    st.markdown("Phase 2 · Module L · Neural Net Basics")

# ── model not trained yet guard ───────────────────────────────────────────────
if not MODEL_PATH.exists():
    st.warning("⚠️ No trained model found. Run `uv run python train.py` first, then refresh.")
    st.stop()

from predict import predict, load_model  # noqa: E402 — after guard

# ── canvas ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Draw here")
    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=18,
        stroke_color="white",
        background_color="black",
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
        display_toolbar=True,
    )

with col2:
    st.subheader("Prediction")
    if canvas_result.image_data is not None:
        img_array = canvas_result.image_data[:, :, :3]          # drop alpha
        gray = np.mean(img_array, axis=2).astype(np.uint8)       # (280,280)
        # Resize to 28×28
        pil_img = Image.fromarray(gray, mode="L").resize((28, 28), Image.LANCZOS)
        arr28 = np.array(pil_img)

        if arr28.max() > 10:                                      # ignore blank canvas
            digit = predict(arr28)
            st.markdown(f"## {digit}")
            st.caption("predicted digit")

            # confidence bar chart
            import torch
            from model import DigitNet
            import torchvision.transforms as T

            model = load_model()
            t = T.Compose([T.ToTensor(), T.Normalize((0.1307,), (0.3081,))])
            tensor = t(pil_img).unsqueeze(0)
            with torch.no_grad():
                probs = torch.softmax(model(tensor), dim=1).squeeze().numpy()

            import pandas as pd
            st.bar_chart(pd.DataFrame({"probability": probs}, index=list(range(10))))
        else:
            st.info("Start drawing to see a prediction")
    else:
        st.info("Start drawing to see a prediction")

# ── preview 28×28 ─────────────────────────────────────────────────────────────
if canvas_result.image_data is not None:
    with st.expander("What the model sees (28×28)"):
        img_array = canvas_result.image_data[:, :, :3]
        gray = np.mean(img_array, axis=2).astype(np.uint8)
        pil_small = Image.fromarray(gray, mode="L").resize((28, 28), Image.LANCZOS)
        pil_big   = pil_small.resize((140, 140), Image.NEAREST)
        st.image(np.array(pil_big), caption="28×28 input to the network", clamp=True)
