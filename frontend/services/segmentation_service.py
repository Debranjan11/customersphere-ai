from services.api_client import api_client


class SegmentationService:

    # ----------------------------------
    # Train Model
    # ----------------------------------

    def train_model(
        self,
        token,
    ):

        return api_client.post(
            "/segmentation/train",
            token=token,
        )

    # ----------------------------------
    # Predict Segments
    # ----------------------------------

    def predict_segments(
        self,
        token,
    ):

        return api_client.get(
            "/segmentation/predict",
            token=token,
        )


segmentation_service = SegmentationService()