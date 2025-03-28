from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from app.database import *
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from app.database import Base
 
 
 # this is the Alembic Config object, which provides
 # access to the values within the .ini file in use.
config = context.config
from app.config import settings

ssh_tunnel = SSHTunnelForwarder(
(settings.SSH_HOST, settings.SSH_PORT),
ssh_username=settings.SSH_USER,
ssh_password=settings.SSH_KEY,  # Use a private key file if required
remote_bind_address=(settings.DB_HOST, settings.DB_PORT),
)

import time

ssh_tunnel.start()
time.sleep(2)  

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:{ssh_tunnel.local_bind_port}/{settings.DB_NAME}"

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# from app.model.qna_ques import Questions
from app.model.candidate import Candidate
from app.model.client import Client
from app.model.postion import Position
from app.model.question_master import QuestionsMaster
from app.model.user import User
from app.model.panel import Panel
 
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    # with connectable.connect() as connection:
    #     context.configure(
    #         connection=connection, target_metadata=target_metadata
    #     )

    #     with context.begin_transaction():
    #         context.run_migrations()
    with ssh_tunnel:  # Ensure the SSH tunnel is running
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
    ssh_tunnel.stop()
else:
    run_migrations_online()
    ssh_tunnel.stop()
