from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from sqlmodel import SQLModel
from database import engine
from api import router  
from model import load_model


# Lifespan 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 데이터베이스 테이블 생성
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info(f"Tables in metadata: {SQLModel.metadata.tables.keys()}") 

        # 모델 로드 구현
        logger.info("Loading the AI model...")
        load_model(r"C:\Users\KimGunwoo\Desktop\catch_my_mind\model\best_model.pt")  # 실제 경로로 대체
    except Exception as e:
        logger.error(f"Error during app startup: {e}")
        raise e  # 예외 발생 시 FastAPI 실행 중단
    yield  # lifespan 종료 후 cleanup 가능
    logger.info("Application shutting down.")

# FastAPI 애플리케이션 초기화
app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우트 추가
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hello world!"}

# 실행 엔트리포인트
if __name__ == "__main__":
    import uvicorn

    # 개발 환경에서는 reload=True로 코드 변경 사항 반영
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
