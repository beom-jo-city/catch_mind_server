import albumentations as A

augmentations = {
    # 회전 및 반전
    "rotate": A.Rotate(limit=45, p=1.0),  # 45도 회전
    "flip": A.HorizontalFlip(p=1.0),     # 좌우 반전
    "vertical_flip": A.VerticalFlip(p=1.0),  # 상하 반전

    # 밝기 및 대비 조정
    "brightness": A.RandomBrightnessContrast(p=1.0),  # 밝기/대비 조정
    "gamma": A.RandomGamma(p=1.0),  # 감마 조정

    # 색상 및 픽셀 조작
    "blur": A.Blur(blur_limit=7, p=1.0),  # 블러 효과
    "motion_blur": A.MotionBlur(blur_limit=7, p=1.0),  # 모션 블러 효과
    "sharpen": A.Sharpen(p=1.0),  # 이미지 샤프닝
    "invert": A.InvertImg(p=1.0),  # 색상 반전
    "solarize": A.Solarize(threshold=128, p=1.0),  # 태양광 효과 (임계값 기준)
    "clahe": A.CLAHE(p=1.0),  # CLAHE (히스토그램 균등화)
    "posterize": A.Posterize(num_bits=4, p=1.0),  # 포스터화

    # 노이즈 추가
    "gaussian_noise": A.GaussNoise(var_limit=(10.0, 50.0), p=1.0),  # 가우시안 노이즈
    "iso_noise": A.ISONoise(p=1.0),  # ISO 노이즈
    "multiplicative_noise": A.MultiplicativeNoise(multiplier=(0.9, 1.1), p=1.0),  # 곱셈 노이즈

    # 기하학적 변환
    "scale": A.RandomScale(scale_limit=0.2, p=1.0),  # 무작위 스케일링
    "shift": A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=0, p=1.0),  # 이동 및 회전
    "elastic_transform": A.ElasticTransform(alpha=1, sigma=50, p=1.0),  # 탄성 변형
    "perspective": A.Perspective(scale=(0.05, 0.1), p=1.0),  # 원근법 변형
    "grid_distortion": A.GridDistortion(p=1.0),  # 그리드 왜곡
    "optical_distortion": A.OpticalDistortion(distort_limit=0.2, shift_limit=0.2, p=1.0),  # 광학적 왜곡

    # 자르기 및 패딩
    "random_crop": A.RandomCrop(width=256, height=256, p=1.0),  # 임의 자르기
    "center_crop": A.CenterCrop(width=256, height=256, p=1.0),  # 중앙 자르기
    "resize": A.Resize(height=256, width=256, p=1.0),  # 크기 조정
    "pad": A.PadIfNeeded(min_height=300, min_width=300, border_mode=0, p=1.0),  # 패딩 추가

    # 기타 효과
    "grid_dropout": A.GridDropout(p=1.0),  # 무작위 그리드 삭제
    "superpixels": A.Superpixels(p_replace=0.5, n_segments=100, p=1.0),  # Superpixel 효과
}
