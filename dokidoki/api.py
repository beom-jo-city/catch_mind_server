from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from crud import get_leaderboard, add_score
from database import get_session
from pydantic import BaseModel
from schemas import LeaderboardRequest, LeaderboardResponse, PredictRequest, PredictResponse, AugmentationRequest, Response
from PIL import Image
import os
from utils import apply_augmentation
from collections import defaultdict

router = APIRouter()

# issue : 어그멘테이션 변수로 둘지 DB에 올릴지 프론트에서 해치울지
# issue : 사용자 리더보드에 rank 포함해서 뱉기로 수정
# issue : 모델이랑 합치기 

user_augmentation = defaultdict(str) # 사용자별로 기억해둬야함... 여럿이서 동시에 하면 덮어씌워지므로 

def set_augmentation(request: AugmentationRequest):
    user_augmentation["user"] = request.augmentation  # 키는 사용자별 고유 ID로 대체 가능
    return request.augmentation


# 키워드 및 증강 조건 서버에 저장하는게 아니라 음... 음...  증강조건만 기억해뒀다가 이따 모델 예측할때 써먹기 
@router.post("/api/receive-keyword")
async def receive_augmentation(request: AugmentationRequest):
    try:
        set_augmentation(request)
        return Response(message="Keyword and augmentation received successfully")
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
@router.post("/receive-image")
async def predict(request: PredictRequest, session: Session = Depends(get_session)) -> list[PredictResponse]:
    if not request.filename.endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG allowed.")

    if not os.path.exists(request.image):
        raise HTTPException(status_code=400, detail="File does not exist.")
    try:
        image = Image.open(request.image) 

        augImage = apply_augmentation(image=image, augmentation=augmentation) # async def receive_augmentation(request: AugmentationRequest)에 들어있는 augmentation 변수를 쓰고 싶다


        # model = get_model() 모델 로드
        # predictions = model(augImage) 모델 예측측

        # 예측 결과 변환
        return [
            PredictResponse(classname = prediction.classname, score = prediction.score)
            for prediction in predictions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
# 어 생각해보니까 db에 저장 해야 돼? 바로 보여주면 되는 거 아님???
# 모델 추론 결과 겟 이거 필요해? 
# 아 crud 필요 없겟구나 아항...