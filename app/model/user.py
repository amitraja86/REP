import uuid
 
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer,JSON,Text
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import Base
from app.utils.helper_functions import get_current_time

class User(Base):
    __tablename__ = "user_detail"

    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    # id =Column(Integer,primary_key=True,nullable=False,unique=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255) ,nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_current_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.id or str(uuid.uuid4())