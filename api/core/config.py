from os import environ
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()


class Config:
    environment = environ["ENVIRONMENT"]
    database_url = environ["DB_POSTGRES_URL"]
    token_url = environ["TOKEN_URL"]
    jwt_secret = environ["JWT_SECRET"]
    jwt_algorithm = environ["JWT_ALGORITHM"]
    access_token_exp_mins = environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
    log_level = environ["LOG_LEVEL"]
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app_config = Config()
