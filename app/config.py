import boto3
from pydantic_settings import BaseSettings
import subprocess


class Settings(BaseSettings):
    DATABASE_URL: str
    SSH_HOST :str 
    SSH_PORT :int 
    SSH_USER :str
    SSH_KEY :str
    DB_PORT :int 
    DB_HOST:str
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD :str
    SECRET_KEY :str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
      
    class Config:
        env_file = ".env"


settings = Settings()

