from typing import List
from api.database.interfaces.repository_interface import IRepository
from api.database.models import Customer
from api.schemas.customer import CustomerCreate, CustomerUpdate
from api.services.interfaces.customer_service_interface import ICustomerService
from api.utils.exceptions import ExceptionHandler


class CustomerService(ICustomerService):
    def __init__(self, customer_repository: IRepository[Customer]) -> None:
        self._customer_repository = customer_repository

    async def create_customer(self, customer: CustomerCreate) -> Customer:
        if await self.find_customer(name=customer.name):
            ExceptionHandler.raise_http_exception(409, "Customer already exists")

        db_customer = Customer(name=customer.name, details=customer.details)
        return await self._customer_repository.create(db_customer)

    async def update_customer(
        self, customer_id: str, customer: CustomerUpdate
    ) -> Customer:
        if await self.find_customer(name=customer.name):
            ExceptionHandler.raise_http_exception(409, "Customer name already exists")

        db_customer = await self.find_customer(customer_id=customer_id)

        if db_customer is None:
            ExceptionHandler.raise_http_exception(404, "Customer not found")

        updates = customer.model_dump()
        return await self._customer_repository.update(
            db_customer, updates=updates, load_relations=["projects"]
        )

    async def get_customer(
        self,
        name: str | None = None,
        customer_id: str | None = None,
        projects: bool = False,
        users: bool = False,
    ) -> Customer:
        if not name and not customer_id:
            ExceptionHandler.raise_http_exception(
                400, "No customer name or ID provided"
            )

        customer = await self.find_customer(
            name=name,
            customer_id=customer_id,
            load_relations=["projects"] if projects else None,
        )

        if not customer:
            ExceptionHandler.raise_http_exception(404, "Customer not found")

        if users and projects:
            await self.load_users([customer])
        return customer

    async def list_customers(
        self, projects: bool = False, users: bool = False
    ) -> List[Customer]:
        customers = await self._customer_repository.list_all(
            load_relations=["projects"] if projects else None
        )

        if not users or not projects:
            return customers

        await self.load_users(customers)
        return customers

    async def find_customer(
        self,
        load_relations: List[str] | None = None,
        name: str | None = None,
        customer_id: str | None = None,
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
            params=params, and_condition=False, load_relations=load_relations
        )
        if not result:
            return None
        return result[0]

    async def delete_customer(self, customer_id) -> None:
        customer = await self.find_customer(customer_id=customer_id)
        if customer is None:
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        await self._customer_repository.delete(customer)

    async def load_users(self, customers: List[Customer]) -> None:
        for customer in customers:
            if customer.projects:
                for project in customer.projects:
                    await project.awaitable_attrs.users
