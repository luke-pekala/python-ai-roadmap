"""Train DigitNet on MNIST and save weights to models/mnist.pth."""
import pathlib
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from model import DigitNet

MODELS_DIR = pathlib.Path(__file__).parent / "models"
DATA_DIR   = pathlib.Path(__file__).parent / "data"
EPOCHS     = 10
BATCH_SIZE = 64
LR         = 1e-3


def get_loaders():
    t = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    train_ds = datasets.MNIST(DATA_DIR, train=True,  download=True, transform=t)
    test_ds  = datasets.MNIST(DATA_DIR, train=False, download=True, transform=t)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False)
    return train_loader, test_loader


def train() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model     = DigitNet().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    train_loader, test_loader = get_loaders()

    for epoch in range(1, EPOCHS + 1):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # Evaluate
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                preds = model(images).argmax(dim=1)
                correct += (preds == labels).sum().item()
                total   += labels.size(0)
        acc = correct / total
        print(f"Epoch {epoch:>2}/{EPOCHS}  loss={running_loss/len(train_loader):.4f}  test_acc={acc:.4f}")

    save_path = MODELS_DIR / "mnist.pth"
    torch.save(model.state_dict(), save_path)
    print(f"\nModel saved → {save_path}")


if __name__ == "__main__":
    train()
