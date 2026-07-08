from pathlib import Path

import joblib
from sklearn.cluster import KMeans

import pandas as pd
import matplotlib.pyplot as plt

from backend.ml.segmentation.utils import (
    save_label_mapping,
)
from backend.constants.segmentation import (
    CHAMPIONS,
    LOYAL_CUSTOMERS,
    BIG_SPENDERS,
    POTENTIAL_LOYALISTS,
    AT_RISK,
    LOST_CUSTOMERS,
)

MODEL_DIR = Path("model_registry/segmentation")
MODEL_PATH = MODEL_DIR / "kmeans.pkl"


class CustomerSegmentationModel:

    def __init__(self, n_clusters=5):

        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10,
        )

    def train(self, features):

        labels = self.model.fit_predict(features)

        return labels

    def save(self):

        MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            self.model,
            MODEL_PATH
        )

    def load(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"KMeans model not found: {MODEL_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)

        return self

    def predict(self, features):

        return self.model.predict(features)
    
    #elbow method

def generate_elbow_plot(features):

        inertia = []

        cluster_range = range(2, 11)

        for k in cluster_range:

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10,
            )

            model.fit(features)

            inertia.append(model.inertia_)

        MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        plot_path = MODEL_DIR / "elbow_curve.png"

        plt.figure(figsize=(8, 5))

        plt.plot(cluster_range, inertia, marker="o")

        plt.xlabel("Number of Clusters")

        plt.ylabel("Inertia")

        plt.title("Elbow Method")

        plt.grid(True)

        plt.savefig(plot_path)

        plt.close()

        return plot_path
    
    #generate segment mapping
def generate_segment_mapping(dataframe, model):

        dataframe = dataframe.copy()

        dataframe["cluster"] = model.labels_

        summary = (
            dataframe.groupby("cluster")
            .agg(
                recency=("recency", "mean"),
                frequency=("frequency", "mean"),
                monetary=("monetary", "mean"),
            )
            .reset_index()
        )

        # Normalize metrics
        summary["recency_score"] = (
            summary["recency"].max() - summary["recency"]
        ) / (
            summary["recency"].max() - summary["recency"].min() + 1e-9
        )

        summary["frequency_score"] = (
            summary["frequency"] - summary["frequency"].min()
        ) / (
            summary["frequency"].max() - summary["frequency"].min() + 1e-9
        )

        summary["monetary_score"] = (
            summary["monetary"] - summary["monetary"].min()
        ) / (
            summary["monetary"].max() - summary["monetary"].min() + 1e-9
        )

        # Final weighted business score
        summary["business_score"] = (
            0.4 * summary["monetary_score"]
            + 0.35 * summary["frequency_score"]
            + 0.25 * summary["recency_score"]
        )

        summary = summary.sort_values(
            by="business_score",
            ascending=False,
        ).reset_index(drop=True)

        labels = [
            CHAMPIONS,
            LOYAL_CUSTOMERS,
            BIG_SPENDERS,
            POTENTIAL_LOYALISTS,
            AT_RISK,
            LOST_CUSTOMERS,
        ]

        mapping = {}

        for i, row in summary.iterrows():

            cluster = int(row["cluster"])

            if i < len(labels):

                mapping[str(cluster)] = labels[i]

            else:

                mapping[str(cluster)] = (
                    f"Segment {cluster}"
                )

        save_label_mapping(mapping)

        return mapping