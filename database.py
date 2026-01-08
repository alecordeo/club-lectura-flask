import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Render usa postgres:// y SQLAlchemy necesita postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}  # 🔴 OBLIGATORIO EN RENDER
    )
else:
    # LOCAL
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5435/club_lectura",
        echo=False,
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()