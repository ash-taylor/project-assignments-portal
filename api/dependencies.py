from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import Depends
from jwt import InvalidTokenError
from api.database.crud import get_user_by_username
from api.database.database import SessionLocal
from api.schemas.auth import TokenData
from api.schemas.user import UserCreate, UserHashed
from api.utils.auth import auth_handler
from api.utils.exceptions import ExceptionHandler


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password_dep(user: UserCreate) -> UserHashed:
    user_dict = user.model_dump()
    user_dict.update({"hashed_password": auth_handler.hash_password(user.password)})
    return UserHashed(**user_dict)


def get_current_user_dep(
    token: Annotated[str, Depends(auth_handler.oauth2_schema)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = auth_handler.decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            ExceptionHandler.raise_credentials_exception()
        token_data = TokenData(username=username)
    except InvalidTokenError:
        ExceptionHandler.raise_credentials_exception()
    user = get_user_by_username(db, username=token_data.username).scalar()
    if user is None:
        ExceptionHandler.raise_credentials_exception()
    return user
