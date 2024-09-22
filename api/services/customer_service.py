"""The Service layer for all customer API routes"""

import logging
from typing import List

from api.database.interfaces.repository_interface import IRepository
from api.database.models import Customer
from api.schemas.customer import CustomerCreate, CustomerUpdate
from api.services.interfaces.customer_service_interface import ICustomerService
from api.utils.exceptions import (
    AttributeNotFoundError,
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    DatabaseConnectionError,
    ExceptionHandler,
    IntegrityViolationError,
    RepositoryError,
)


logger = logging.getLogger(__name__)


class CustomerService(ICustomerService):
    """The service for all customer routes.
    Contains all business logic

    Args:
        ICustomerService: Interface defining required functionalities
    """

    def __init__(self, customer_repository: IRepository[Customer]) -> None:
        """Initialize the service

        Args:
            customer_repository (IRepository[Customer]): The repository layer for database interactions
        """
        logger.info("Initializing CustomerService")
        self._customer_repository = customer_repository

    async def create_customer(self, customer: CustomerCreate) -> Customer:
        """Functionality for 'Customer' entity creation and storage

        Args:
            customer (CustomerCreate): Validated Pydantic CustomerCreate model

        Returns:
            Customer: The successfully stored and created customer
        """

        try:
            logger.info("Creating customer")
            # Check whether customer with same name exists
            if await self.find_customer(name=customer.name):
                raise CustomerAlreadyExistsError

            logger.info("Customer does not exist")

            # Create a customer database model
            db_customer = Customer(name=customer.name, details=customer.details)
            logger.info("Customer created")
            return await self._customer_repository.create(db_customer)
        except CustomerAlreadyExistsError as e:
            logger.error("Customer already exists: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def update_customer(
        self, customer_id: str, customer: CustomerUpdate
    ) -> Customer:
        """Functionality for updating an existing customer entity

        Args:
            customer_id (str): The ID of customer to update
            customer (CustomerUpdate): Validated Pydantic CustomerUpdate model

        Returns:
            Customer: Updated customer
        """

        try:
            # Get the existing customer entity from DB
            db_customer = await self.find_customer(customer_id=customer_id)

            # Check requested customer exists
            if db_customer is None:
                raise CustomerNotFoundError
            logger.info("Customer found")

            logger.info("Updating customer")
            return await self._customer_repository.update(
                db_customer, updates=customer.model_dump(), load_relations=["projects"]
            )
        except CustomerNotFoundError as e:
            logger.error("Customer not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        except IntegrityViolationError as e:
            logger.error("Integrity violation: %s", e)
            ExceptionHandler.raise_already_exists_exception()
        except AttributeNotFoundError as e:
            logger.error("Attribute not found: %s", e)
            ExceptionHandler.raise_http_exception(400, "Customer not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def get_customer(
        self,
        name: str | None = None,
        customer_id: str | None = None,
        projects: bool = False,
        users: bool = False,
    ) -> Customer:
        """Functionality for retrieving a customer entity from database

        Args:
            name (str | None, optional): Name of customer to find. Defaults to None.
            customer_id (str | None, optional): ID of customer to find. Defaults to None.
            projects (bool, optional): Include customer's related projects? Defaults to False.
            users (bool, optional): Include customer's related users? Defaults to False.
            Only applicable if projects loaded.

        Returns:
            Customer: Retrieved customer entity
        """
        try:
            logger.info("Getting customer")
            if not name and not customer_id:
                raise ValueError("Either name or customer id must be provided")

            customer = await self.find_customer(
                name=name,
                customer_id=customer_id,
                load_relations=["projects"] if projects else None,
            )

            if not customer:
                raise CustomerNotFoundError
            logger.info("Customer found")
            if users and projects:
                logger.info("Loading users")
                await self.load_users([customer])
            return customer
        except CustomerNotFoundError as e:
            logger.error("Customer not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        except ValueError as e:
            logger.error("Value error: %s", e)
            ExceptionHandler.raise_http_exception(400, "Bad request")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def list_customers(
        self, projects: bool = False, users: bool = False
    ) -> List[Customer]:
        """Functionality for listing all customers in the database.

        Args:
            projects (bool, optional): Include customer's related projects? Defaults to False.
            users (bool, optional): Include customer's related users? Defaults to False.
            Only applicable if projects loaded.

        Returns:
            List[Customer]: A list containing all customer entities
        """

        try:
            logger.info("Listing customers")
            customers = await self._customer_repository.list_all(
                load_relations=["projects"] if projects else None
            )

            if len(customers) < 1 or not users or not projects:
                return customers

            logger.info("Loading relations")
            await self.load_users(customers)
            return customers
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def find_customer(
        self,
        load_relations: List[str] | None = None,
        name: str | None = None,
        customer_id: str | None = None,
    ) -> Customer | None:
        """Functionality for finding a customer in the database.

        Customer can be found by either name or ID.

        Args:
            load_relations (List[str] | None, optional): Dict containing any related entities
            to load async. Defaults to None.
            name (str | None, optional): Name of customer to find. Defaults to None.
            customer_id (str | None, optional): ID of customer to find. Defaults to None.

        Returns:
            Customer | None: The found customer entity or None
        """

        try:
            logger.info("Finding customer")

            # Build a dict of params to query for, required by repository layer
            params = {
                key: value
                for key, value in {
                    "id": customer_id,
                    "name": name,
                }.items()
                if value is not None
            }
            if not params:
                logger.error("No parameters provided")
                raise ValueError("No parameters provided")

            result = await self._customer_repository.find(
                params=params, and_condition=False, load_relations=load_relations
            )
            if not result:
                return None

            logger.info("Customer found")
            return result[0]
        except ValueError as e:
            logger.error("Value error: %s", e)
            ExceptionHandler.raise_http_exception(400, "Bad request")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def delete_customer(self, customer_id: str) -> None:
        """Functionality to find and delete a customer entity

        Args:
            customer_id (str): The ID of the customer to delete

        """
        try:
            logger.info("Deleting customer")
            customer = await self.find_customer(customer_id=customer_id)

            if customer is None:
                raise CustomerNotFoundError
            logger.info("Customer found")
            await self._customer_repository.delete(customer)
        except CustomerNotFoundError as e:
            logger.error("Customer not found: %s", e)
            ExceptionHandler.raise_http_exception(404, "Customer not found")
        except DatabaseConnectionError as e:
            logger.error("Database connection error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except RepositoryError as e:
            logger.error("Repository error: %s", e)
            ExceptionHandler.raise_internal_server_error()
        except Exception as e:
            logger.error("Error creating user: %s", e)
            ExceptionHandler.raise_internal_server_error()

    async def load_users(self, customers: List[Customer]) -> None:
        """Helper function to load any required related users async.

        Args:
            customers (List[Customer]): A list containing customer entities
        """
        for customer in customers:
            if customer.projects:
                for project in customer.projects:
                    await project.awaitable_attrs.users
