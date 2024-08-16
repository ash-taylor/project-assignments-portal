import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("Unable to resolve Database URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
