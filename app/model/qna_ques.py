import uuid
 
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey, Integer,JSON,Text
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import Base
from app.utils.helper_functions import get_current_time


class Questions(Base):
    __tablename__ = "questions"

    id = Column(
        String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    Candidate_name = Column(String(255),nullable=True)
    designation =Column(String(255),nullable=True)
    L1_Client =Column(String(255),nullable=True)
    End_Client=Column(String(255),nullable=True)
    Positions=Column(Integer,nullable=True)
    Location=Column(String(255),nullable=True)
    Source_type=Column(String(255),nullable=True)
    Interview_Panel=Column(JSON, default=[], nullable=True)
    Round=Column(Integer,nullable=True)
    Status=Column(String(255),nullable=True)
    question = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_current_time)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.id or str(uuid.uuid4())
    
    @classmethod
    def get_all_questions(cls, db:Session):
        return db.query(cls).all()

    @classmethod
    def get_question_by_id(cls, db: Session, question_id: str):
        return db.query(cls).filter(cls.id == question_id).first()
    
    # @classmethod
    # def get_question_by_panel(cls,db:Session,panel_name:str):
    #     query = db.query(cls)
    #     if panel_name:
    #         query = query.filter(cls.Interview_Panel.ilike(f"%{panel_name}%"))
        
    #     query = query.order_by(cls.created_at.desc())
    #     results = query.all()

    #     return results
    
    @classmethod
    def get_question_by_company_position(cls,db:Session,company_name:str,position:str,panel_name:str):
        query = db.query(cls)
        if company_name:
            query = query.filter(   
                        or_(
                            cls.L1_Client.ilike(f"%{company_name}%"),
                            cls.End_Client.ilike(f"%{company_name}%")
                        )
            )
        if position:
            query = query.filter(cls.designation.ilike(f"%{position}%"))
        if panel_name:
            query = query.filter(cls.Interview_Panel.ilike(f"%{panel_name}%"))


        query = query.order_by(cls.created_at.desc())
        results = query.all()

        return results
    
    @classmethod
    def create_question(cls, db, **kwargs):
        question = cls(**kwargs)
        db.add(question)
        db.commit()
        db.refresh(question)
        return question