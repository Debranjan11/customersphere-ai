from backend.ml.segmentation.clustering import (
    CustomerSegmentationModel,
)

from backend.ml.segmentation.preprocessing import (
    SegmentationPreprocessor,
)

from backend.ml.segmentation.utils import (
    load_label_mapping,
)

def predict_segments(rfm_dataframe):

    preprocessor = SegmentationPreprocessor()

    preprocessor.load()

    features = preprocessor.transform(
        rfm_dataframe
    )

    model = CustomerSegmentationModel()

    model.load()

    clusters = model.predict(
        features
    )

    rfm_dataframe["cluster"] = clusters

    mapping = load_label_mapping()

    rfm_dataframe["segment"] = (
        rfm_dataframe["cluster"]
        .astype(str)
        .map(mapping)
    )

    return rfm_dataframe