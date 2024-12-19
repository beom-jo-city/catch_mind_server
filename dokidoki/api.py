from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from crud import get_leaderboard, add_score
from database import get_session
from pydantic import BaseModel
from schemas import LeaderboardRequest, LeaderboardResponse, PredictRequest, PredictResponse, AugmentationRequest, Response
from PIL import Image
import os
from utils import apply_augmentation, class_name_changer
from collections import defaultdict

from model import get_model
import torch.nn.functional as F
from fastapi.responses import JSONResponse
from io import BytesIO
import torch
import base64

# 전역변수
keyword = None
augmentation = None

router = APIRouter()

user_augmentation = defaultdict(str) # 사용자별로 기억해둬야함... 여럿이서 동시에 하면 덮어씌워지므로 

# 키워드 및 증강 조건 서버에 저장하는게 아니라 음... 음...  증강조건만 기억해뒀다가 이따 모델 예측할때 써먹기 
@router.post("/api/receive-keyword")
async def receive_augmentation(request: AugmentationRequest):
    try:
        global keyword, augmentation  # 전역변수 선언
        keyword = request.keyword
        augmentation = request.augmentation
        
        user_augmentation["user"] = request.augmentation
        return JSONResponse(content={"message":"Keyword and augmentation received successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process request: {e}")

# 리더보드 상위 10개 닉네임-스코어 내림차순으로 반환 
@router.get("/api/leaderboard")
def read_leaderboard(session: Session = Depends(get_session)) -> list[LeaderboardResponse]: # 세션관리를 알아서 하게 함 lifespan에 맞춰서 자동으로 열고닫고 굳
    return get_leaderboard(session)

# 닉네임-스코어 db에 저장 
@router.post("/submit-userinfo")
def create_score(request: LeaderboardRequest, session: Session = Depends(get_session)) -> Response:
    return add_score(session, request)

# 사용자가 그린 이미지를 가져와서 증강거쳐서서 모델에 넣고 예측 하고 결과까지 한번에 얻기 
@router.post("/api/receive-image")
async def predict(request: PredictRequest):
    # 1. Base64 문자열에서 헤더와 데이터를 분리
    try:
        if "," in request.image:
            header, encoded = request.image.split(",", 1)
        else:
            encoded = request.image  # 헤더가 없는 경우
    except:
        return {"error": f"Invalid Base64 encoding: {str(e)}"}

    # 2. Base64 디코딩
    try:
        image_data = base64.b64decode(encoded)
    except base64.binascii.Error as e:
        return {"error": f"Invalid Base64 encoding: {str(e)}"}
    
    try:
        # 이미지 수정
        image = Image.open(BytesIO(image_data)).convert('RGB')
        augImage = apply_augmentation(image=image, augmentation=augmentation) # async def receive_augmentation(request: AugmentationRequest)에 들어있는 augmentation 변수를 쓰고 싶다
        
        top_predictions = []  # List to store top 5 predictions for each input
        top_confidences = []  # List to store confidence scores of top 5 predictions

        # 모델 예측
        model = get_model()
        
        with torch.no_grad():  # Disable gradient calculation
            # Move data to the same device as the model
            images = augImage
            
            # Perform prediction through the model
            logits = model(images)
            probabilities = F.softmax(logits, dim=1)  # Calculate probabilities using softmax

            # Get top 5 predictions and their confidence scores
            top5_probs, top5_preds = torch.topk(probabilities, k=10, dim=1)

            # # Convert results to lists and store them
            top_predictions.extend(top5_preds.cpu().detach().numpy().flatten().tolist())
            top_confidences.extend(top5_probs.cpu().detach().numpy().flatten().tolist())
            # print(top_predictions)
            
            # 클래스 숫자 -> 문자
            top_predictions_str = class_name_changer(top_predictions)
            
        # 예측 결과 변환
        return JSONResponse(
            content={
                "message":"Prediction successfully",
                "results": [
                    top_predictions_str,  # 리스트  ex) ['전원 콘센트', '선', '고래', '손전등', '랜턴', '오리', '가스렌지', '항공모함', '랍스터', '개']
                    top_confidences  # 리스트  ex) [0.1, 0.4, 0.5, ...]
                ]
            }
        )
        # return JSONResponse(content={"message":"model received successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")