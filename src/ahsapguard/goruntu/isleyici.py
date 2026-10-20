import numpy as np
import torch
from PIL import Image
from torchvision import transforms

# ResNet18 için standart ImageNet dönüşümleri
STANDART_DONUSUM = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        ),
    ]
)


def goruntu_yukle_ve_islemden_gecir(goruntu_yolu: str) -> torch.Tensor:
    """Görüntüyü diskten okur, doğrular ve PyTorch model girdisi formatına (1, 3, 224, 224) dönüştürür."""
    try:
        img = Image.open(goruntu_yolu).convert("RGB")
        tensor_img = STANDART_DONUSUM(img)
        return tensor_img.unsqueeze(0)  # Batch boyutu ekle: (1, C, H, W)
    except Exception as e:
        raise ValueError(
            f"Görüntü okuma hatası ('{goruntu_yolu}'): {str(e)}"
        )