# import tkinter
# from tkinter import Image
from sqlmodel import SQLModel, Field
from pydantic import BaseModel 
from typing import List

class AugmentationRequest(BaseModel):
    keyword: str
    augmentation: str

class Response(BaseModel):
    statusCode: int
    message: str
    
class PredictResult(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    classname: str
    score: float

class PredictRequest(BaseModel):
    image: str

class PredictResponse(BaseModel):
    classname: str
    score: float

class Leaderboard(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nickname: str
    total_score: int
    submission_time: str


class LeaderboardRequest(BaseModel):
    nickname: str
    total_score: int
    submission_time: str

class LeaderboardResponse(BaseModel):
    rank: int
    nickname: str
    score: float

    class Config:
        orm_mode = True