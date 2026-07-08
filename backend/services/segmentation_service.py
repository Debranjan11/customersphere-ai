from backend.repositories.segmentation_repository import (
    SegmentationRepository,
)

from backend.ml.segmentation.feature_engineering import (
    calculate_rfm,
    add_rfm_scores,
)

from backend.ml.segmentation.dataset import (
    export_dataset,
)

from backend.ml.segmentation.train import (
    train_segmentation_model,
)

from backend.ml.segmentation.predict import (
    predict_segments as predict_customer_clusters,
)


class SegmentationService:

    def __init__(self, db):

        self.repo = SegmentationRepository(db)

    def _build_rfm_dataset(
        self,
        org_id: int,
        export_csv: bool = False,
    ):

        data = self.repo.get_rfm_data(org_id)

        rfm = calculate_rfm(data)

        rfm = add_rfm_scores(rfm)

        if export_csv:
            export_dataset(rfm)

        return rfm

    def train_model(
        self,
        org_id: int,
    ):

        rfm = self._build_rfm_dataset(
            org_id,
            export_csv=True,
        )

        return train_segmentation_model(rfm)
    
    def _to_business_response(self, dataframe):

        records = dataframe.to_dict(
            orient="records"
        )

        return [
            {
                "customer_id": row["customer_id"],
                "customer_name": row["customer_name"],
                "recency": row["recency"],
                "frequency": row["frequency"],
                "monetary": row["monetary"],
                "cluster": row["cluster"],
                "segment": row["segment"],
            }
            for row in records
        ]

    def predict_segments(
        self,
        org_id: int,
    ):

        rfm = self._build_rfm_dataset(
            org_id
        )

        predictions = predict_customer_clusters(
            rfm
        )

        return self._to_business_response(predictions)
            