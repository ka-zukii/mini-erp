import os
from sqlalchemy import create_engine
from alembic import context
from sqlalchemy import pool
from logging.config import fileConfig
from shared.database.db import Base
from dotenv import load_dotenv

import shared.models.barang
import shared.models.kategori
import shared.models.gudang
import shared.models.pengguna
import shared.models.log_aktivitas
import shared.models.supplier

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = f'postgresql://{os.environ.get("DATABASE_URL")}'
    if not url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = f'postgresql://{os.environ.get("DATABASE_URL")}'
    if not url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()