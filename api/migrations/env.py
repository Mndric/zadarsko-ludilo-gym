import os
import sys
from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Točno postavljanje putanje da Alembic vidi tvoj 'api' folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. IMPORTI TVOJIH MODELA - Prilagođeno tvojim datotekama
from core.database import Base
from models.user import User
from models.training import Training      # Dodano
from models.reservation import Reservation  # Dodano
# Ako imaš ove datoteke, ostavi ih, ako nemaš - zakomentiraj ih:
# from models.membership import Membership 
# from models.equipment import Equipment

# Alembic Config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ciljani metadata iz tvog Base-a
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Pomoćna funkcija za izvršavanje migracija."""
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        render_as_batch=True # Korisno za SQLite/Postgres promjene
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Asinkrono povezivanje na bazu."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Za asinkroni rad unutar postojećeg loopa ili novog
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Ako je loop već pokrenut
        loop.create_task(run_async_migrations())
    else:
        asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()