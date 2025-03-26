import uuid
 
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer,JSON,Text
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import Base

class Client(Base):
    __tablename__ = "CLIENT_MASTER"

    ID = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    NAME = Column(String(255),nullable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ID = self.ID or str(uuid.uuid4())

    @classmethod
    def create_client(cls,db:Session,**kwargs):
        new_response = cls(**kwargs)
        db.add(new_response)
        db.commit()
        db.refresh(new_response)
        return new_response

    @classmethod
    def get_clients(cls, db:Session):
        return db.query(cls).all()
    
    @classmethod
    def get_id(cls,name:str,db:Session):
        return db.query(cls).filter(cls.NAME.ilike(f"%{name}%")).first()
    
    @classmethod
    def get_name(cls,id:str,db:Session):
        return db.query(cls).filter(cls.ID == id).first()
    