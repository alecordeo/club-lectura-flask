import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Render / producción
DATABASE_URL = os.environ.get("DATABASE_URL")

# Soporte local si no existe la variable (opcional)
if DATABASE_URL is None:
    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5435/club_lectura"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
