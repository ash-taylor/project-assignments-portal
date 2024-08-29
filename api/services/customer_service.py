from typing import List
from api.database.interfaces.repository_interface import IRepository
from api.database.models import Customer
from api.schemas.customer import CustomerCreate
from api.services.interfaces.customer_service_interface import ICustomerService
from api.utils.exceptions import ExceptionHandler


class CustomerService(ICustomerService):
    def __init__(self, customer_repository: IRepository[Customer]) -> None:
        self._customer_repository = customer_repository

    async def create_customer(self, customer: CustomerCreate) -> Customer:
        existing_customer = await self.find_customer(name=customer.name)
        if existing_customer:
            ExceptionHandler.raise_http_exception(409, "Customer already exists")
        db_customer = Customer(name=customer.name, details=customer.details)
        return await self._customer_repository.create(db_customer)

    async def get_customer(
        self, name: str | None = None, customer_id: str | None = None
    ) -> Customer:
        if not name and not customer_id:
            ExceptionHandler.raise_http_exception(
                400, "No customer name or ID provided"
            )
        customer = await self.find_customer(name=name, customer_id=customer_id)
        if not customer:
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        return customer

    async def list_customers(self) -> List[Customer]:
        return await self._customer_repository.list_all()

    async def find_customer(
        self, name: str | None = None, customer_id: str | None = None
    ) -> Customer | None:
        params = {
            key: value
            for key, value in {
                "id": customer_id,
                "name": name,
            }.items()
            if value is not None
        }
        result = await self._customer_repository.find(
            params=params, and_condition=False
        )
        if not result:
            return None
        return result[0]

    async def delete_customer(self, customer_id) -> None:
        customer = await self.find_customer(customer_id=customer_id)
        if customer is None:
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        await self._customer_repository.delete(customer)
