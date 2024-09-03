from abc import ABC, abstractmethod
from typing import List, Optional

from api.database.models import Customer
from api.schemas.customer import CustomerCreate, CustomerUpdate


class ICustomerService(ABC):
    @abstractmethod
    async def create_customer(self, customer: CustomerCreate) -> Customer:
        pass

    @abstractmethod
    async def update_customer(
        self, customer_id: str, customer: CustomerUpdate
    ) -> Customer:
        pass

    @abstractmethod
    async def list_customers(
        self, projects: bool = False, users: bool = False
    ) -> List[Customer]:
        pass

    @abstractmethod
    async def get_customer(
        self,
        name: str | None = None,
        customer_id: str | None = None,
        projects: bool = False,
        users: bool = False,
    ) -> Customer:
        pass

    @abstractmethod
    async def find_customer(
        self,
        load_relations: List[str] | None = None,
        name: str | None = None,
        customer_id: str | None = None,
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    async def delete_customer(self, customer_id) -> None:
        pass
