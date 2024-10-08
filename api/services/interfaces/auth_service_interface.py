from abc import ABC, abstractmethod

from fastapi.security import OAuth2PasswordRequestForm

from api.schemas.auth import Token, TokenData


class IAuthService(ABC):
    """Service interface for Auth Service

    Defines necessary functions for inheriting service
    """

    @abstractmethod
    async def login(self, request: OAuth2PasswordRequestForm) -> Token:
        pass

    @abstractmethod
    def hash_pwd(self, pt_pwd: str) -> str:
        pass

    @abstractmethod
    def validate_pwd(self, pt_pwd: str, hashed_pwd: str) -> bool:
        pass

    @abstractmethod
    def create_jwt(self, data: dict) -> str:
        pass

    @abstractmethod
    def decode_jwt(self, token: str) -> TokenData:
        pass
