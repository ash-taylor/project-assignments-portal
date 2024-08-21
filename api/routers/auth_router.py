from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_db_session_dep
from api.schemas.auth import Token
from api.utils.auth import auth_handler
from api.utils.exceptions import ExceptionHandler


router = APIRouter()


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session_dep),
):
    user = await auth_handler.authenticate_user(request, db)

    if not user:
        ExceptionHandler.raise_http_exception(
            401, "Invalid username or password", auth_error=True
        )

    access_token = auth_handler.create_access_token(
        data={"sub": user.user_name, "admin": user.admin}
    )

    return Token(access_token=access_token, token_type="Bearer")
