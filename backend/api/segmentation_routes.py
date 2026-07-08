from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db

from backend.dependencies.auth import get_current_user

from backend.services.segmentation_service import (
    SegmentationService
)

from backend.schemas.segmentation import (
    TrainingSummary,
    CustomerSegment,
)

router = APIRouter(
    prefix="/segmentation",
    tags=["Customer Segmentation"]
)


# @router.get("/generate-dataset")
# def generate_dataset(
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):

#     service = SegmentationService(db)

#     return service.generate_dataset(
#         current_user.org_id
#     )

#training endpoint
@router.post(
    "/train",
    response_model=TrainingSummary,
)
def train_model(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = SegmentationService(db)

    return service.train_model(
        current_user.org_id
    )

#prediction endpoint
@router.get(
    "/predict",
    response_model=list[CustomerSegment],
)
def predict_customer_segments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = SegmentationService(db)

    return service.predict_segments(
        current_user.org_id
    )