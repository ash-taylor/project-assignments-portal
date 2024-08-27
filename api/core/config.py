from os import environ
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SQLALCHEMY_DATABASE_URL = environ["DB_POSTGRES_URL"]
TOKEN_URL = environ["TOKEN_URL"]
JWT_SECRET = environ["JWT_SECRET"]
JWT_ALGORITHM = environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = environ["ACCESS_TOKEN_EXPIRE_MINUTES"]


class Config:
    database_url = environ["DB_POSTGRES_URL"]
    token_url = environ["TOKEN_URL"]
    jwt_secret = environ["JWT_SECRET"]
    jwt_algorithm = environ["JWT_ALGORITHM"]
    access_token_exp_mins = environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
    log_level = environ["LOG_LEVEL"]
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app_config = Config()
