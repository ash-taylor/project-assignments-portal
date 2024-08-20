import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CURRENT_DIR = Path(__file__).resolve().parent
ENV_PATH = CURRENT_DIR.parent.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)

SQLALCHEMY_DATABASE_URL = os.getenv("DB_POSTGRES_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Unable to resolve Database URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
