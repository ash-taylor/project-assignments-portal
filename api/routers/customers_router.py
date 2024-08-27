import logging
from typing import Annotated, List
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_customer_service,
    validate_admin,
    validate_user,
)
from api.schemas.auth import TokenData
from api.schemas.customer import CustomerCreate, CustomerOut
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


@router.get("/customer", tags=["customers"], response_model=CustomerOut)
async def get_customer(
    token: Annotated[TokenData, Depends(validate_user)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
    customer_id: str | None = None,
    name: str | None = None,
):
    logger.info("user: %s invoked GET /customer", token.username)
    return await customer_service.get_customer(name, customer_id=customer_id)


@router.get("/customers", tags=["customers"], response_model=(List[CustomerOut] | None))
async def get_all_customers(
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
):
    logger.info("user: %s invoked GET /customers", token.username)
    return await customer_service.list_customers()


@router.delete("/customer/{customer_id}", tags=["customers"], status_code=204)
async def delete_customer(
    customer_id: str,
    token: Annotated[TokenData, Depends(validate_admin)],  # Requires admin rights
    customer_service: Annotated[ICustomerService, Depends(get_customer_service)],
):
    logger.info("user: %s invoked DELETE /customer/%s", token.username, customer_id)
    await customer_service.delete_customer(customer_id=customer_id)
