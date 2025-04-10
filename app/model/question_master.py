import uuid
 
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer,JSON,Text
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from app.database import Base
from app.utils.helper_functions import get_current_time


class QuestionsMaster(Base):
    __tablename__ = "QUESTION_"

    ID = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    Candidate_name = Column(String(255),nullable=False)
    position_id =Column(String(255), ForeignKey("POSITION_MASTER.ID", ondelete = "CASCADE"),nullable=False)
    client_id =Column(String(255), ForeignKey("CLIENT_MASTER.ID", ondelete = "CASCADE"),nullable=False)
    End_Client=Column(String(255),nullable=True)
    Positions=Column(Integer,nullable=True,default=0)
    Location=Column(String(255),nullable=True,default="Remote")
    Source_type=Column(String(255),nullable=True,default="By Client")
    Country=Column(String(255),nullable=True,default="Unknown")
    Interview_Panel=Column(JSON, default=[], nullable=False)
    Interview_starttime=Column(DateTime, nullable=False, default=get_current_time)
    Interview_stoptime=Column(DateTime, nullable=False, default=lambda: get_current_time() + timedelta(minutes=40))
    Round=Column(Integer,default=1,nullable=True)
    Status=Column(String(255),nullable=False)
    question = Column(Text, nullable=False)
    # created_at = Column(DateTime, nullable=False, default=get_current_time)

    
    @classmethod
    def get_all_questions(cls, db:Session):
        return db.query(cls).all()

    # @classmethod
    # def get_question_by_id(cls, db: Session, question_id: str):
    #     return db.query(cls).filter(cls.id == question_id).first()
    
    # @classmethod
    # def get_question_by_panel(cls,db:Session,panel_name:str):
    #     query = db.query(cls)
    #     if panel_name:
    #         query = query.filter(cls.Interview_Panel.ilike(f"%{panel_name}%"))
        
    #     query = query.order_by(cls.created_at.desc())
    #     results = query.all()

    #     return results
    
    @classmethod
    def get_question(cls,db:Session,client_id:str,position_id:str,panel_name:str,candidate:str):
        query = db.query(cls)
        if client_id:
            query = query.filter(cls.client_id == client_id)
        if position_id:
            query = query.filter(cls.position_id == position_id)
        if panel_name :
            query = query.filter(cls.Interview_Panel.ilike(f"%{panel_name}%"))
        if candidate:
            query=query.filter(cls.Candidate_name==candidate)


        query = query.order_by(cls.Interview_starttime.desc())
        results = query.all()

        return results
    
    @classmethod
    def create_question(cls, db:Session, **kwargs):
        question = cls(**kwargs)
        db.add(question)
        db.commit()
        db.refresh(question)
        return question