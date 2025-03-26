from datetime import datetime
import pytz
import pandas as pd
from fastapi import HTTPException,status


def get_current_time():
     return (
         datetime.utcnow()
         .replace(tzinfo=pytz.utc)
         .astimezone(pytz.timezone("Asia/Kolkata"))
     )
def is_csv(content_type: str) -> bool:
    return content_type == "text/csv"


def parse_functional_questions_from_new_csv(csv_file):
    try:
        csv_data = []

        # Read the csv file
        df = pd.read_csv(csv_file.file, encoding='utf-8')

        # Replace NaN values with empty strings
        df.fillna("", inplace=True)
        
        # extracting details from the csv
        for index, row in df.iterrows():

            data = {
                "question":row["Question"],
                "Candidate_name":row["Candidate name"],
                "designation":row["Position"],
                "L1_Client":row["L1 Client"],
                "End_Client":row["End-Client"],
                "Positions":row["No. of Position"],
                "Location":row["Location"],
                "Source_type":row["Source type"],
                "Interview_Panel":row["Interview Panel"],
                "Interview_start_time":row["INTERVIEW_START_DATE_TIME"],
                "Interview_stop_time":row["INTERVIEW_END_DATE_TIME"],
                "Round":row["Round"],
                "Status":row["Status"],
            }
            csv_data.append(data)
            
        return csv_data 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing the csv file {str(e)}")

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

