from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET, TOKEN_URL
from api.database.crud import get_user_by_username


class AuthHandler:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

    def validate_password(self, pt_pwd: str, hashed_pwd: str):
        return self._pwd_context.verify(pt_pwd, hashed_pwd)

    def authenticate_user(self, request: OAuth2PasswordRequestForm, db: Session):
        user = get_user_by_username(db, request.username).scalar_one_or_none()

        if not user or not self.validate_password(
            request.password, user.hashed_password
        ):
            return None

        print(user)

        return user

    def hash_password(self, pt_pwd: str):
        return self._pwd_context.hash(pt_pwd)

    def create_access_token(self, data: dict):
        assert ACCESS_TOKEN_EXPIRE_MINUTES is not None, ACCESS_TOKEN_EXPIRE_MINUTES
        assert JWT_SECRET is not None, JWT_SECRET
        assert JWT_ALGORITHM is not None, JWT_ALGORITHM

        to_encode = data.copy()
        exp = datetime.now(timezone.utc) + timedelta(float(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": exp})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str):
        assert JWT_ALGORITHM is not None, JWT_ALGORITHM
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


auth_handler = AuthHandler()
