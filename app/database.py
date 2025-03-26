from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool
from sshtunnel import SSHTunnelForwarder


from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# create a base class
Base = declarative_base()


# class DBSession:
#     def __init__(self):
#         engine = create_engine(
#             SQLALCHEMY_DATABASE_URL,
#             poolclass=pool.QueuePool,
#             pool_size=10000,
#             max_overflow=8000,
#         )
#         SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#         self.db = SessionLocal()

#     def __enter__(self):
#         return self.db

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.db.close()


# def get_db():
#     with DBSession() as db:
#         yield db


def get_db() -> Session:
    ssh_tunnel = SSHTunnelForwarder(
    (settings.SSH_HOST, settings.SSH_PORT),
    ssh_username=settings.SSH_USER,
    ssh_password=settings.SSH_KEY,  # Use a private key file if required
    remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
    )
    # ssh_tunnel.stop() 
    ssh_tunnel.start()

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:{ssh_tunnel.local_bind_port}/{settings.DB_NAME}"
    print(SQLALCHEMY_DATABASE_URL)

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10000,
        max_overflow=8000,
        # pool_recycle=3600
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    engine.connect()
    db = SessionLocal()
    
    try:
        return db
    finally:
        db.close()
        


class DBFactory:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = get_db()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db:
            self.db.close()
