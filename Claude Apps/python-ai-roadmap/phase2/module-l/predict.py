"""Load trained model and predict a single image (numpy array 28x28, 0-255)."""
import pathlib
import numpy as np
import torch
from torchvision import transforms

from model import DigitNet

MODEL_PATH = pathlib.Path(__file__).parent / "models" / "mnist.pth"

_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])


def load_model() -> DigitNet:
    model = DigitNet()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
    model.eval()
    return model


_model: DigitNet | None = None


def predict(image_array: np.ndarray) -> int:
    """
    Predict digit from a 28x28 uint8 numpy array (grayscale, 0-255).
    Returns integer 0-9.
    """
    global _model
    if _model is None:
        _model = load_model()

    from PIL import Image
    img = Image.fromarray(image_array.astype(np.uint8), mode="L")
    tensor = _transform(img).unsqueeze(0)          # (1, 1, 28, 28)
    with torch.no_grad():
        logits = _model(tensor)
    return int(logits.argmax(dim=1).item())
