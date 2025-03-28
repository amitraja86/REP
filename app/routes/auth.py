from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils.helper_functions import *
from app.utils.oauth import *
from app.database import *
from app.schemas.qna_question import *
from app.model.user import User


router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):

    try:
    # hash the password - user.password
        with DBFactory() as db:
            hashed_password = hash(user.password)
            user.password = hashed_password

            new_user = User(email=user.email,username=user.username,password_hash=user.password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            

            return new_user
    
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error



@router.get('/login/', response_model=Token, status_code=status.HTTP_200_OK)
def login(email:str,password:str):
    try:
        with DBFactory() as db:
            user = db.query(User).filter(
                User.email == email).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

            if not verify(password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


            access_token = create_access_token(data={"user_id": user.id})

            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as error:
        raise error

    # Step 7: Handle unexpected errors
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
