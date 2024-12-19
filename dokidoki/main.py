from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
import threading
from api import router

app = FastAPI()
app.include_router(router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 외부 요청 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 설정
@app.get("/")
def read_root():
    return {"message": "Hello from LocalTunnel!"}


# LocalTunnel 실행 함수
def start_localtunnel():
    # LocalTunnel을 실행하고 고정된 서브도메인을 생성
    process = subprocess.Popen(
        ["lt", "--port", "8000", "--subdomain", "cv05-catchmind"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    for line in iter(process.stdout.readline, b""):
        print(line.decode(), end="")

# Uvicorn 실행 함수
def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 두 개의 스레드를 사용하여 LocalTunnel과 Uvicorn 실행
tunnel_thread = threading.Thread(target=start_localtunnel)
tunnel_thread.start()

server_thread = threading.Thread(target=start_uvicorn)
server_thread.start()