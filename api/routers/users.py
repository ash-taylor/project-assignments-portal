from typing import Annotated, List
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from api.database import crud
from api.dependencies import get_current_user_dep, get_db, hash_password_dep
from api.schemas.user import UserBase, UserHashed, UserOut
from api.utils.exceptions import ExceptionHandler

router = APIRouter(prefix="/api")


@router.post("/user", tags=["users"], response_model=UserOut)
def create_user(
    user: UserHashed = Depends(hash_password_dep), db: Session = Depends(get_db)
):
    db_user = crud.check_user_exists(db, user.user_name, user.email)

    if db_user:
        if db_user.user_name == user.user_name and db_user.email == user.email:
            ExceptionHandler.raise_http_exception(400, "User already exists")
        elif db_user.user_name == user.user_name:
            ExceptionHandler.raise_http_exception(400, "Username already exists")
        elif db_user.email == user.email:
            ExceptionHandler.raise_http_exception(400, "Email already exists")

    return crud.create_user(db=db, user=user)


@router.get("/users", tags=["users"], response_model=List[UserOut])
async def read_users(db: Session = Depends(get_db)):
    db_users = crud.get_all_users(db)
    return db_users


@router.get("/users/me", tags=["users"], response_model=UserOut)
async def read_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user_dep)]
):
    return current_user
