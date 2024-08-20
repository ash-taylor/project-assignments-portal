from os import getenv
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = getenv("DB_POSTGRES_URL")
TOKEN_URL = getenv("TOKEN_URL")
JWT_SECRET = getenv("JWT_SECRET")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
