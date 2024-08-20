from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from api.database.models import User
from api.schemas.user import UserHashed


def create_user(db: Session, user: UserHashed):
    user_dict = user.model_dump()
    db_user = User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.execute(select(User).filter(User.user_name == username))


def get_user_by_email(db: Session, email: str):
    return db.execute(select(User).filter(User.email == email))


def check_user_exists(db: Session, username: str, email: str):
    return db.execute(
        select(User).where(or_(User.email == email, User.user_name == username))
    ).scalar()


def get_all_users(db: Session):
    return db.execute(select(User)).scalars().all()
