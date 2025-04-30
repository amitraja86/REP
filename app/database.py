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


def get_db() -> Session:
    ssh_tunnel = SSHTunnelForwarder(
        (settings.SSH_HOST, settings.SSH_PORT),
        ssh_username=settings.SSH_USER,
        ssh_password=settings.SSH_KEY,  # or private key
        remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
    )
    ssh_tunnel.start()

    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:{ssh_tunnel.local_bind_port}/{settings.DB_NAME}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_recycle=280,
        pool_pre_ping=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        ssh_tunnel.stop()
        
class DBFactory:
    def __enter__(self):
        self.db_gen = get_db()
        self.db = next(self.db_gen)
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, "db_gen"):
            self.db_gen.close()
