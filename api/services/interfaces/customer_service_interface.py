from abc import ABC, abstractmethod
from typing import List, Optional

from api.database.models import Customer
from api.schemas.customer import CustomerCreate


class ICustomerService(ABC):
    @abstractmethod
    async def create_customer(self, customer: CustomerCreate) -> Customer:
        pass

    @abstractmethod
    async def list_customers(self) -> List[Customer]:
        pass

    @abstractmethod
    async def get_customer(
        self,
        name: str | None = None,
        customer_id: str | None = None,
    ) -> Customer:
        pass

    @abstractmethod
    async def find_customer(
        self,
        name: str | None = None,
        customer_id: str | None = None,
    ) -> Optional[Customer]:
        pass

    @abstractmethod
    async def delete_customer(self, customer_id) -> None:
        pass
