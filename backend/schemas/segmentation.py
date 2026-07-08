from pydantic import BaseModel
from typing import Dict, List


class TrainingSummary(BaseModel):

    customers_processed: int

    clusters: int

    model_path: str

    scaler_path: str

    elbow_plot: str

    cluster_distribution: Dict[int, int]


class CustomerSegment(BaseModel):

    customer_id: int

    customer_name: str

    recency: int

    frequency: int

    monetary: float

    cluster: int

    segment : str