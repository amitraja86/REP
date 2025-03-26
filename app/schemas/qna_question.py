from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username:str
    password: str

class Question(BaseModel):
    question: str
    Candidate_name:str
    designation:str
    L1_Client:str
    End_Client:str
    Positions:int
    Location:str
    Source_type:str
    Interview_Panel:list
    Interview_start_time:str
    Interview_stop_time :str
    Round:int
    Status:str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    id: Optional[str] = None

class CandidateCreate(BaseModel):
    ID:str
    NAME:str
    CONTACT:Optional[int] =None
    ROLE:Optional[str]=None

class Config:
    from_attributes = True