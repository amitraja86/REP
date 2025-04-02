from pydantic import BaseModel,EmailStr,model_validator
from datetime import datetime
from typing import Optional
import json

class UserCreate(BaseModel):
    email: EmailStr
    username:str
    password: str

class Question(BaseModel):
    question: Optional[str]=None
    Candidate_name:str
    designation:str
    L1_Client:str
    End_Client:str
    Positions:Optional[int]=None
    Location:Optional[str]=None
    Source_type:Optional[str]=None
    Country:str
    Interview_Panel:str
    Interview_start_time:str
    duration :int
    Round:Optional[int]=None
    Status:str
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
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