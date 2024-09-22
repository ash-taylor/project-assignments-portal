"""'Customers' router module providing entry point for all 'customer' API routes."""

import logging
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_customer_service,
    parse_customer_id,
    parse_optional_customer_id,
    validate_admin,
    validate_user,
)
from api.schemas.auth import TokenData
from api.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from api.schemas.relationships import (
    CustomerWithProjectsOut,
    CustomerWithProjectsUsersOut,
)
from api.services.interfaces.customer_service_interface import ICustomerService


router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/customer", tags=["customers"], response_model=CustomerOut)
async def create_customer(
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    customer: CustomerCreate,
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
):
    """POST /customer route

    Validates and creates a new customer in the database,

    Args:
        token (Annotated[TokenData, Depends): JWT,
        customer (CustomerCreate): The customer object - validated by the CustomerCreate model.
        customer_service (Annotated[ICustomerService, Depends): The application customer service.

    Returns:
        Customer: The updated customer entity - validated against the CustomerOut model.
    """

    logger.info("user: %s invoked POST /customer", token.username)
    return await customer_service.create_customer(customer)


@router.get(
    "/customer",
    tags=["customers"],
    response_model=Union[
        CustomerOut | CustomerWithProjectsOut | CustomerWithProjectsUsersOut
    ],
)
async def get_customer(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    customer_id: Annotated[str | None, Depends(parse_optional_customer_id)],
    name: str | None = None,
    projects: bool = False,
    users: bool = False,
):
    """GET /customer route

    Looks for and returns a specified customer by id or name.
    Provides option to return the customer with related projects and users.

    Args:
        token (Annotated[TokenData, Depends): JWT
        customer_service (Annotated[ICustomerService, Depends): Customer service
        customer_id (Annotated[str  |  None, Depends): The customer ID to search for.
        name (str | None, optional): The customer name to search for. Defaults to None.
        projects (bool, optional): Set True if customer related 'Projects' required in the response.
        Defaults to False.
        users (bool, optional): Set True if customer related 'Users' required in the response..
        Defaults to False.

    Returns:
       Customer: The updated customer entity - validated against the CustomerOut model.
    """

    logger.info("user: %s invoked GET /customer", token.username)
    return await customer_service.get_customer(
        name=name, customer_id=customer_id, projects=projects, users=users
    )


@router.get(
    "/customers",
    tags=["customers"],
    response_model=List[
        Union[CustomerOut | CustomerWithProjectsOut | CustomerWithProjectsUsersOut]
    ],
)
async def get_all_customers(
    token: Annotated[TokenData, Depends(validate_user)],  # User
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    projects: bool = False,
    users: bool = False,
):
    """GET /customers route

    Returns all customer entities in the database.

    Args:
        token (Annotated[TokenData, Depends): JWT
        customer_service (Annotated[ICustomerService, Depends): Customer service
        projects (bool, optional): Set True if customer related 'Projects' required in the response.
        Defaults to False.
        users (bool, optional): Set True if customer related 'Users' required in the response.
        Defaults to False.

    Returns:
       List[Customer]: A list of all customer entities in the database.
    """

    logger.info("user: %s invoked GET /customers", token.username)
    return await customer_service.list_customers(projects, users)


@router.put("/customer/{customer_id}", tags=["customers"], response_model=CustomerOut)
async def update_customer(
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    customer_id: Annotated[str, Depends(parse_customer_id)],
    customer: CustomerUpdate,
):
    """PUT /customer/{customer_id} route

    Looks for and updates an existing customer entity with the requested updates
    (validated against the CustomerUpdate model)

    Args:
        token (Annotated[TokenData, Depends): JWT
        customer_service (Annotated[ICustomerService, Depends): Customer service
        customer_id (Annotated[str, Depends): Customer Service
        customer (CustomerUpdate): The customer request validated against the CustomerCreate model

    Returns:
        Customer: The updated customer entity
    """

    logger.info("user: %s invoked PUT /customers/%s", token.username, customer_id)
    return await customer_service.update_customer(
        customer_id=customer_id, customer=customer
    )


@router.delete("/customer/{customer_id}", tags=["customers"], status_code=204)
async def delete_customer(
    customer_id: Annotated[str, Depends(parse_customer_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Admin
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
):
    """DELETE /customer/{customer_id} route

    Looks for and deletes an existing customer entity.

    Args:
        customer_id (Annotated[str, Depends): ID of customer to delete
        token (Annotated[TokenData, Depends): JWT
        customer_service (Annotated[ICustomerService, Depends): Customer service

    Returns:
        None: A 204 response returned to client if successful.
    """

    logger.info("user: %s invoked DELETE /customer/%s", token.username, customer_id)
    await customer_service.delete_customer(customer_id=customer_id)
