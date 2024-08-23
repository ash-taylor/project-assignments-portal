import logging
from typing import Annotated, List
from fastapi import APIRouter, Depends

from api.dependencies import get_auth_service_dep, get_customer_service_dep
from api.schemas.customer import CustomerCreate, CustomerOut
from api.services.auth_service import oauth2_scheme
from api.services.interfaces.auth_service_interface import IAuthService
from api.services.interfaces.customer_service_interface import ICustomerService
from api.utils.exceptions import ExceptionHandler


router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.post("/customer", tags=["customers"], response_model=CustomerOut)
async def create_customer(
    token: Annotated[str, Depends(oauth2_scheme)],
    customer: CustomerCreate,
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service_dep)],
):
    if not auth_service.is_admin(token):
        ExceptionHandler.raise_http_exception(
            401, "User unauthorized to create customer", auth_error=True
        )
    return await customer_service.create_customer(customer)


@router.get("/customer", tags=["customers"], response_model=CustomerOut)
async def get_customer(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service_dep)],
    customer_id: str | None = None,
    name: str | None = None,
):
    logger.info("GET /customer?customer_id=%s&name=%s", customer_id, name)
    auth_service.validate_user(token)

    return await customer_service.find_customer(
        name=name if name else None, customer_id=customer_id if customer_id else None
    )


@router.get("/customers", tags=["customers"], response_model=(List[CustomerOut] | None))
async def get_all_customers(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service_dep)],
):
    auth_service.validate_user(token)

    return await customer_service.list_customers()


@router.delete("/customer/{customer_id}", tags=["customers"], status_code=204)
async def delete_customer(
    customer_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[IAuthService, Depends(get_auth_service_dep)],
    customer_service: Annotated[ICustomerService, Depends(get_customer_service_dep)],
):
    if not auth_service.is_admin(token):
        ExceptionHandler.raise_http_exception(
            401, "User unauthorized to create customer", auth_error=True
        )
    await customer_service.delete_customer(customer_id=customer_id)
