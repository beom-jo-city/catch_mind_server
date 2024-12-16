from fastapi import HTTPException
from sqlmodel import Session, select
from schemas import Leaderboard, LeaderboardRequest, LeaderboardResponse, PredictRequest, PredictResponse, PredictResult

# async def predict(session: Session, request: PredictRequest):
#     # 모델 load
#     model = 
#     # 예측 결과 뽑기 ( 클래스명-스코어 리스트 )
#     prediction = 

#     # 예측한 결과를 DB에 저장
#     # session.add(prediction)
#     # session.commit()
#     # session.refresh(prediction)
#     return PredictResponse(prediction)
    

# 리더보드 상위 15개의 데이터 반환환 rank 추가 
def get_leaderboard(session: Session, limit: int = 10):
    try:
        # query = session.query(Leaderboard).order_by(Leaderboard.score.desc()).limit(15)
        # leaderboard = query.all()
        # return leaderboard
        query = select(Leaderboard).order_by(Leaderboard.score.desc()).limit(limit)
        # ㄴ 스코어에 대해 내림차순 정렬해서 10개 끊어서 선택 
        return session.exec(query).all() # 쿼리를 실행하고 정렬된 데이터를 리스트 형태로 반환 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leaderboard: {e}")
    

# 리더보드에 스코어/닉네임 추가 
def add_score(session: Session, request: LeaderboardRequest):
    new_entry = Leaderboard(nickname=request.nickname, score=request.score)
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    return LeaderboardResponse(nickname=new_entry.nickname, score=new_entry.score)