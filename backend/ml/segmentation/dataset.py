import os


def export_dataset(df):

    os.makedirs(
        "data/training",
        exist_ok=True
    )

    path = "data/training/rfm_dataset.csv"

    df.to_csv(
        path,
        index=False
    )

    return path