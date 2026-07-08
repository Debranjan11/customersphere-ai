from pathlib import Path

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler


MODEL_DIR = Path("model_registry/segmentation")
SCALER_PATH = MODEL_DIR / "scaler.pkl"


class SegmentationPreprocessor:

    def __init__(self, feature_columns=None):

        self.scaler = StandardScaler()

        self.feature_columns = (
            feature_columns
            or [
                "recency",
                "frequency",
                "monetary",
            ]
        )

    def fit_transform(self, dataframe: pd.DataFrame):

        features = dataframe[self.feature_columns]

        return self.scaler.fit_transform(features)

    def transform(self, dataframe: pd.DataFrame):

        features = dataframe[self.feature_columns]

        return self.scaler.transform(features)

    def save(self):

        MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            self.scaler,
            SCALER_PATH
        )

    def load(self):

        if not SCALER_PATH.exists():
            raise FileNotFoundError(
                f"Scaler not found at {SCALER_PATH}. Train the model first."
            )

        self.scaler = joblib.load(SCALER_PATH)

        return self
