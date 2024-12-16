# import tkinter
# from tkinter import Image
from sqlmodel import SQLModel, Field
from pydantic import BaseModel 

class AugmentationRequest(BaseModel):
    augmentation: str

class AugmentationResponse(BaseModel):
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
    score: float

class LeaderboardRequest(BaseModel):
    nickname: str
    score: float

class LeaderboardResponse(BaseModel):
    id: int
    nickname: str
    score: float

    class Config:
        orm_mode = True