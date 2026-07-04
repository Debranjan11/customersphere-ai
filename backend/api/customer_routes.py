from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.dependencies import (
    require_manager,
    require_analyst,
)

from backend.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse,
)

from backend.services.customer_service import CustomerService

from typing import Optional

from backend.schemas import MessageResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

#create customer
@router.post(
    "/",
    response_model=CustomerResponse,
)
def create_customer(
    request: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = CustomerService(db)

    return service.create_customer(
        request,
        current_user.org_id,
    )

#get all customer
@router.get("/",
    response_model=CustomerListResponse,
    )
def get_all_customers(
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        is_active: bool = True,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        db: Session = Depends(get_db),
        current_user=Depends(require_analyst),
    ):

    service = CustomerService(db)

    return service.get_all_customers(
        current_user.org_id,
        page,
        page_size,
        keyword,
        city,
        state,
        is_active,
        sort_by,
        sort_order,
    )

#get customer by id
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = CustomerService(db)

    return service.get_customer(
        customer_id,
        current_user.org_id,
    )

#update customer
@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    request: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = CustomerService(db)

    return service.update_customer(
        customer_id,
        request,
        current_user.org_id,
    )

#delete customer
@router.delete(
    "/{customer_id}",
    response_model=MessageResponse,
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = CustomerService(db)

    return service.delete_customer(
        customer_id,
        current_user.org_id,
    )

#search customer
@router.get("/search/")
def search_customers(
    keyword: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = CustomerService(db)

    return service.search_customers(
        keyword,
        current_user.org_id,
    )