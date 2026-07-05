from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.dependencies import (
    require_manager,
    require_analyst,
)

from backend.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
)

from backend.schemas.common import MessageResponse

from backend.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

#create transaction
@router.post(
    "/",
    response_model=TransactionResponse,
)
def create_transaction(
    request: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = TransactionService(db)

    return service.create_transaction(
        request,
        current_user.org_id,
    )

#get all transactions
@router.get(
    "/",
    response_model=TransactionListResponse,
)
def get_all_transactions(
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    category: str | None = None,
    payment_method: str | None = None,
    status: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    sort_by: str = "transaction_date",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = TransactionService(db)

    return service.get_all_transactions(
        current_user.org_id,
        page,
        page_size,
        keyword,
        category,
        payment_method,
        status,
        start_date,
        end_date,
        sort_by,
        sort_order,
    )

#get transaction by id
@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = TransactionService(db)

    return service.get_transaction(
        transaction_id,
        current_user.org_id,
    )

#update transaction
@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: int,
    request: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = TransactionService(db)

    return service.update_transaction(
        transaction_id,
        request,
        current_user.org_id,
    )

#delete transaction
@router.delete(
    "/{transaction_id}",
    response_model=MessageResponse,
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_manager),
):

    service = TransactionService(db)

    return service.delete_transaction(
        transaction_id,
        current_user.org_id,
    )

#customer transaction history
@router.get(
    "/customer/{customer_id}",
    response_model=list[TransactionResponse],
)
def get_customer_transactions(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = TransactionService(db)

    return service.get_customer_transactions(
        customer_id,
        current_user.org_id,
    )

@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_analyst),
):

    service = TransactionService(db)

    return service.get_dashboard_summary(
        current_user.org_id
    )