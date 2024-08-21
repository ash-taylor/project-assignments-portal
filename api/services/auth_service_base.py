from abc import ABC, abstractmethod


class AuthServiceBase(ABC):
    @abstractmethod
    def create_jwt(self, data: dict) -> str:
        pass
