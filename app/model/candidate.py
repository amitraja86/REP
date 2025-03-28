import uuid
 
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer,JSON,Text
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import Base

class Candidate(Base):
    __tablename__ = "CANDIDATE_MASTER"

    ID = Column(
        String(36),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    NAME = Column(String(255),nullable=False)
    CONTACT = Column(Integer,nullable=True)
    ROLE =Column(String(50),nullable=True)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.id = self.id or str(uuid.uuid4())

    @classmethod
    def get_all_questions(cls, db:Session):
        return db.query(cls).all()
    
    @classmethod
    def create_candidate(cls,db:Session,**kwargs):
        new_response = cls(**kwargs)
        db.add(new_response)
        db.commit()
        db.refresh(new_response)
        return new_response
    
    @classmethod
    def get_candidate_by_id(cls,db:Session,id):
        return db.query(cls).filter(cls.ID == id).first()
    
    @classmethod
    def get_candidate_by_name(cls,db:Session,name):
        return db.query(cls).filter(cls.NAME==name).first()