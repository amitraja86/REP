
# ssh_tunnel = SSHTunnelForwarder(
# (settings.SSH_HOST, settings.SSH_PORT),
# ssh_username=settings.SSH_USER,
# ssh_pkey=settings.SSH_KEY,  # Use a private key file if required
# remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
# )

# ssh_tunnel.start()
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:{ssh_tunnel.local_bind_port}/{settings.DB_NAME}"

from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import settings
server = SSHTunnelForwarder(
    (settings.SSH_HOST, settings.SSH_PORT),
    ssh_username=settings.SSH_USER,
    ssh_password=settings.SSH_KEY,
    remote_bind_address=(settings.DB_HOST, 3306),
)

try:
    server.start()
    print(f"Tunnel opened at 127.0.0.1:{server.local_bind_port}")
    DATABASE_URL = ("mysql+pymysql://poc:JuYTRETre32DEW2@localhost:%s/poc" % server.local_bind_port)
    # DATABASE_URL ="mysql+pymysql://poc:JuYTRETre32DEW2@localhost:3306/poc"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # If you need thread-safe sessions
    session = scoped_session(SessionLocal)

    # Test database connection
    try:
        with engine.connect() as conn:
            print("Database Connected!")
        
        # Example usage of session
        db = session()
        print("Session created successfully!")

        # Close session properly
        db.close()
    
    except Exception as e:
        print("Connection failed:", e)
    
    server.stop()
except Exception as e:
    print(f"Error: {e}")

from app.utils.helper_functions import get_current_time
from datetime import timedelta
i=get_current_time()
print(i,i+timedelta(minutes=40))