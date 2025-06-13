import sys
import os
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

# Garante que o diretório do projeto está no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import SQLModel  # ajuste o import se estiver em outra pasta
from database import DATABASE_URL

# Alembic Config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def get_url():
    return DATABASE_URL

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    from sqlalchemy import create_engine
    connectable = create_engine(get_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
