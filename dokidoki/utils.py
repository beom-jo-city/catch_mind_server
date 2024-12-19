import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import numpy as np
from augmentation_list import augmentations
import pandas as pd

# 클래스 숫자 -> 문자 변경
def class_name_changer(predictions):
    class_index_df = pd.read_csv(r"C:\Users\KimGunwoo\Desktop\catch_my_mind\model\class_index.csv", encoding='cp949')
    # 클래스 이름
    class_index_dict = dict(zip(class_index_df['ClassIndex'], class_index_df['korean']))  # 영어로 보려면 'ClassName'으로 변경

    # 클래스 이름과 신뢰도 추출
    target_text = [class_index_dict[idx] for idx in predictions]  # 클래스 이름 리스트
    
    return target_text


# 증강 함수  -->  지금 증강 적용 안했습니다. 
def apply_augmentation(image: Image.Image, augmentation: str) -> np.ndarray:
    
    # if augmentation not in augmentations:
    #     raise ValueError(f"Unsupported augmentation: {augmentation}")

    # PIL 이미지를 NumPy로 변환
    image_np = np.array(image, dtype=np.float32)

    # 증강 적용
    # transform = A.Compose([A.Resize(224, 224), augmentations[augmentation], ToTensorV2()])
    transform = A.Compose([A.Resize(224, 224), ToTensorV2()])
    augmented = transform(image=image_np)
    
    # 배치 차원 추가 (1, C, H, W)
    augmented_image = augmented["image"].unsqueeze(0)  # 배치 차원 추가
    return augmented_image
