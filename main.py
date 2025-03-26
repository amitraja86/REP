from fastapi import FastAPI
from app.routes import qna_questions
from app.routes import auth as auth_router
from app.database import Base
import re

# from config.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


class RegexCORSMiddleware(CORSMiddleware):
    def is_allowed_origin(self, origin: str) -> bool:
        for pattern in self.allow_origins:
            if re.fullmatch(pattern, origin):
                return True
        return False


allowed_origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    # "http://localhost:5174",
    r"https://.*\.ambitionhire\.ai",
]

app.add_middleware(
    RegexCORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routers
app.include_router(qna_questions.router)
app.include_router(auth_router.router,prefix="/user")