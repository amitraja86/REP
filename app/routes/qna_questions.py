import csv
import io
from fastapi import APIRouter, HTTPException, status, Body, Query,Depends ,Response,UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List, Optional
from app.schemas.qna_question import Question
from app.model.qna_ques import Questions
from app.model.candidate import Candidate
from app.model.client import Client
from app.model.postion import Position
from app.model.question_master import QuestionsMaster
from app.model.user import User

from app.database import *
from app.utils.helper_functions import *
from app.utils.oauth import *
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/download-csv/", status_code=status.HTTP_200_OK)
def get_all_ques(company_name:Optional[str]=None,position:Optional[str]=None,panel_name:Optional[str]=None,current_user: int = Depends(get_current_user)):
    # Sample data (Replace this with your DB data)
    try:
        with DBFactory() as db:
            client_id=Client.get_id(company_name,db)
            position_id=Position.get_id(position,db)
            data= get_ques_byfilter(client_id,position_id,panel_name)
            filename=""
            if company_name:
                filename+=company_name
            if position:
                filename+=position
            if panel_name:
                filename+=panel_name
            if filename=="":
                filename="data"
            formatted_data = [
                {
                    "Candidate name": ques["Candidate_name"],
                    "Position": ques["Positions"],
                    "L1 Client": ques["L1_Client"],
                    "Question": ques["question"],
                    "End-Client": ques["End_Client"],
                    "No. of Position": ques["No_of_position"],
                    "Location": ques["Location"],
                    "Source type": ques["Source_type"],
                    "Interview Panel": ques["Interview_Panel"],
                    "Round": ques["Round"],
                    "Status": ques["Status"],
                }
                for ques in data["details"]
            ]

            # print(formatted_data)
            # Create an in-memory CSV file
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=formatted_data[0].keys())
            writer.writeheader()
            writer.writerows(formatted_data)

            # Move the cursor to the beginning
            output.seek(0)

            # Return response as a file
            return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}.csv"})


    # Step 6: Handle expected errors
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error

    # return data



@router.get("/question/", status_code=status.HTTP_200_OK)
def get_ques_byfilter(company_name:Optional[str]=None,position:Optional[str]=None,panel_name:Optional[str]=None,current_user: int = Depends(get_current_user)):

    try:
        with DBFactory() as db:
            client_id=Client.get_id(company_name,db)
            position_id=Position.get_id(position,db)
            questions =QuestionsMaster.get_question(db,client_id,position_id,panel_name)
            return_data=[]
            for question in questions:
                client_name = Client.get_name(question.client_id,db)
                position_name = Position.get_name(question.position_id,db)
                data={
                "Candidate_name": question.Candidate_name,
                "L1_Client":client_name.NAME,
                "End_Client":question.End_Client,
                "Positions":position_name.NAME,
                "No_of_position":question.Positions,
                "Location":question.Location,
                "Source_type":question.Source_type,
                "Interview_Panel":question.Interview_Panel,
                "Interview_starttime":question.Interview_starttime,
                "Interview_stoptime":question.Interview_stoptime,
                "Round":question.Round,
                "Status":question.Status,
                "question": question.question,
                }
                return_data.append(data)
            
            return {
                    "message": "Questions retrieved successfully",
                    "details" :return_data
                }
    # Step 6: Handle expected errors
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error  


@router.post(
    "/add_questions/", status_code=status.HTTP_201_CREATED
)
def add_question(questions: Question,question_file:UploadFile=File(None),current_user: int = Depends(get_current_user)):
    try:
        with DBFactory() as db:
            # print(questions)
            client_id=Client.get_id(questions.L1_Client,db)
            position_id=Position.get_id(questions.designation,db)
            if client_id is None:
                print(questions.L1_Client)
                Client.create_client(db,NAME=questions.L1_Client)
            if position_id is None:
                print(questions.designation)
                Position.create_position(db,NAME=questions.designation)
            client_id=Client.get_id(questions.L1_Client,db)
            position_id=Position.get_id(questions.designation,db)
            ques ={
            "Candidate_name": questions.Candidate_name,
            "End_Client":questions.End_Client,
            "Positions":questions.Positions,
            "Location":questions.Location,
            "Source_type":questions.Source_type,
            "Interview_Panel":questions.Interview_Panel,
            "Interview_starttime":questions.Interview_start_time,
            "Interview_stoptime":questions.Interview_stop_time,
            "Round":questions.Round,
            "Status":questions.Status,
            "question": questions.question,
            "position_id":position_id.ID,
            "client_id":client_id.ID,
            }
            QuestionsMaster.create_question(
                    db,**ques
                )
        
        
            return {
                    "message": "Question added successfully",
                }
    
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
  

@router.post("/add_question_by_csv/", status_code=status.HTTP_201_CREATED)
def add_questions_from_csv(csv_file:UploadFile=File(...),current_user: int = Depends(get_current_user)):
        
    try:
        with DBFactory() as db:
            if not is_csv(csv_file.content_type):
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail="Only csv files are supported.",
                )
            csv_data = parse_functional_questions_from_new_csv(csv_file)
            for question_details in csv_data:
                # Questions.create_question(db,**question_details)
                client_id=Client.get_id(question_details["L1_Client"],db)
                position_id=Position.get_id(question_details["designation"],db)
                if client_id is None:
                    Client.create_client(db,NAME=question_details["L1_Client"])
                if position_id is None:
                    Position.create_position(db,NAME=question_details["designation"])
                client_id=Client.get_id(question_details["L1_Client"],db)
                position_id=Position.get_id(question_details["designation"],db)
                ques ={
                "Candidate_name": question_details["Candidate_name"],
                "End_Client":question_details["End_Client"],
                "Positions":question_details["Positions"],
                "Location":question_details["Location"],
                "Source_type":question_details["Source_type"],
                "Interview_Panel":question_details["Interview_Panel"],
                "Interview_starttime":question_details["Interview_start_time"],
                "Interview_stoptime":question_details["Interview_stop_time"],
                "Round":question_details["Round"],
                "Status":question_details["Status"],
                "question": question_details["question"],
                "position_id":position_id.ID,
                "client_id":client_id.ID,
                }
                QuestionsMaster.create_question(
                        db,**ques
                    )
            return {
                        "message": "Question added successfully",
                    }
    
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
    
@router.get("/positions/", status_code=status.HTTP_200_OK)
def get_position():
    try:
        with DBFactory() as db:
            position_infos =Position.get_all(db)
            position_list =[]
            for position in position_infos:
                position_list.append(position.NAME)
            return position_list
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error

@router.get("/company/", status_code=status.HTTP_200_OK)
def get_company():
    try:
        with DBFactory() as db:    
            client_infos= Client.get_clients(db)
            client_list=[]
            for client in client_infos:
                client_list.append(client.NAME)

            return client_list
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
    
@router.post("/candidate/add", status_code=status.HTTP_201_CREATED)
def add_candidate(candidate :CandidateCreate,current_user: int = Depends(get_current_user)):
    try:
        with DBFactory() as db:
            existing_candidate=Candidate.get_candidate_by_id(db,candidate.ID) or None
            if existing_candidate:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="ID belong to other Candidate"
                    )
            Candidate.create_candidate(db,**candidate.model_dump())
    
    
            return {"details":"Successfully candidate created"}
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error

@router.get("/candidate/search", status_code=status.HTTP_200_OK)
def search_candidate(name : Optional[str]=None,id :Optional[str]=None,current_user: int = Depends(get_current_user)):
    try:
        with DBFactory() as db:
            by_name,by_id=None,None
            if name:
                by_name=Candidate.get_candidate_by_name(db,name) 
            by_id=None
            if id:
                by_id=Candidate.get_candidate_by_id(db,id) 
            if by_id and by_name:
                if by_id.NAME !=by_name.NAME:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="ID doesn't belong to given Candidate"
                    )
            elif by_id is None or by_name is None:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, 
                        detail="ID and NAME doesn't match"
                    )
            name=by_id.NAME or by_name.NAME
            return name    
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error