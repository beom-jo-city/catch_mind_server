import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import numpy as np

# 증강 함수
def apply_augmentation(image: Image.Image, augmentation: str) -> np.ndarray:
    # 증강 조건에 따라 처리
    augmentations = {
        "flip": A.HorizontalFlip(p=1.0),
        "rotate": A.Rotate(limit=30, p=1.0),
        "brightness": A.RandomBrightnessContrast(p=1.0),
    }
    if augmentation not in augmentations:
        raise ValueError(f"Unsupported augmentation: {augmentation}")

    # PIL 이미지를 NumPy로 변환
    image_np = np.array(image)

    # 증강 적용
    transform = A.Compose([augmentations[augmentation], ToTensorV2()])
    augmented = transform(image=image_np)
    return augmented["image"]