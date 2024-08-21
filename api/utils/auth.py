from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import app_config
from api.database.crud import get_user_by_username


class AuthHandler:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl=app_config.token_url)

    def validate_password(self, pt_pwd: str, hashed_pwd: str):
        return self._pwd_context.verify(pt_pwd, hashed_pwd)

    async def authenticate_user(
        self, request: OAuth2PasswordRequestForm, db: AsyncSession
    ):
        user = await get_user_by_username(db, request.username)

        if not user or not self.validate_password(
            request.password, user.hashed_password
        ):
            return None

        return user

    def hash_password(self, pt_pwd: str):
        return self._pwd_context.hash(pt_pwd)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        exp = datetime.now(timezone.utc) + timedelta(
            float(app_config.access_token_exp_mins)
        )
        to_encode.update({"exp": exp})
        encoded_jwt = jwt.encode(
            to_encode, app_config.jwt_secret, algorithm=app_config.jwt_algorithm
        )
        return encoded_jwt

    def decode_access_token(self, token: str):
        return jwt.decode(
            token, app_config.jwt_secret, algorithms=[app_config.jwt_algorithm]
        )


auth_handler = AuthHandler()
