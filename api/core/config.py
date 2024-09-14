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
    db_echo = environ["DB_ECHO"]
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    admin_username = environ["ADMIN_USERNAME"]
    admin_password = environ["ADMIN_PASSWORD"]
    admin_email = environ["ADMIN_EMAIL"]
    admin_first_name = environ["ADMIN_FNAME"]
    admin_last_name = environ["ADMIN_LNAME"]


app_config = Config()
