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
    Location:Optional[str]=None
    Source_type:Optional[str]=None
    Country:str
    Interview_Panel:str
    Interview_start_time:str
    duration :int
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