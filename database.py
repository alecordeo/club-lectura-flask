import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ==================================================
# DATABASE URL
# - Render usa la variable de entorno DATABASE_URL
# - Local usa PostgreSQL local si la variable no existe
# ==================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5435"
    DB_NAME = "club_lectura"

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# ==================================================
# SQLAlchemy setup
# ==================================================

engine = create_engine(
    DATABASE_URL,
    echo=False  # 🔴 IMPORTANTE: False en producción
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()