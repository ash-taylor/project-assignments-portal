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
    token: Annotated[TokenData, Depends(validate_user)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    customer_id: Annotated[str | None, Depends(parse_optional_customer_id)],
    name: str | None = None,
    projects: bool = False,
    users: bool = False,
):
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
    token: Annotated[TokenData, Depends(validate_user)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    projects: bool = False,
    users: bool = False,
):
    logger.info("user: %s invoked GET /customers", token.username)
    return await customer_service.list_customers(projects, users)


@router.put("/customer/{customer_id}", tags=["customers"], response_model=CustomerOut)
async def update_customer(
    token: Annotated[TokenData, Depends(validate_admin)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    customer_id: Annotated[str, Depends(parse_customer_id)],
    customer: CustomerUpdate,
):
    logger.info("user: %s invoked PUT /customers/%s", token.username, customer_id)
    return await customer_service.update_customer(
        customer_id=customer_id, customer=customer
    )


@router.delete("/customer/{customer_id}", tags=["customers"], status_code=204)
async def delete_customer(
    customer_id: Annotated[str, Depends(parse_customer_id)],
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
):
    logger.info("user: %s invoked DELETE /customer/%s", token.username, customer_id)
    await customer_service.delete_customer(customer_id=customer_id)
