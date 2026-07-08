from backend.ml.segmentation.clustering import (
    CustomerSegmentationModel,
    generate_elbow_plot,
    MODEL_PATH,
)

from backend.ml.segmentation.preprocessing import (
    SegmentationPreprocessor,
    SCALER_PATH,
)


def train_segmentation_model(rfm_dataframe):

    preprocessor = SegmentationPreprocessor()

    features = preprocessor.fit_transform(
        rfm_dataframe
    )

    preprocessor.save()

    elbow_plot = generate_elbow_plot(features)

    model = CustomerSegmentationModel(
        n_clusters=5
    )

    labels = model.train(features)

    from backend.ml.segmentation.clustering import (
    generate_segment_mapping,
    )
    mapping = generate_segment_mapping(
    rfm_dataframe,
    model.model
    )
    model.save()

    rfm_dataframe["cluster"] = labels

    return {
    "customers_processed": len(rfm_dataframe),
    "clusters": len(set(labels)),
    "model_path": str(MODEL_PATH),
    "scaler_path": str(SCALER_PATH),
    "elbow_plot": str(elbow_plot),
    "cluster_distribution": (
        rfm_dataframe["cluster"]
        .value_counts()
        .sort_index()
        .to_dict()
    ),
    "customers": rfm_dataframe.to_dict(
        orient="records"
    ),
    "segment_mapping":str(mapping)
}