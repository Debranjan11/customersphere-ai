from datetime import datetime

import pandas as pd


def calculate_rfm(records):

    if not records:
        return pd.DataFrame(
            columns=[
                "customer_id",
                "customer_name",
                "recency",
                "frequency",
                "monetary",
            ]
        )

    today = datetime.now().date()

    rows = []

    for record in records:

        rows.append(
            {
                "customer_id": record.customer_id,
                "customer_name": record.customer_name,
                "transaction_date": record.transaction_date,
                "amount": float(record.amount),
            }
        )

    df = pd.DataFrame(rows)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    rfm = (
        df.groupby(
            ["customer_id", "customer_name"],
            as_index=False
        )
        .agg(
            recency=(
                "transaction_date",
                lambda x: (
                    today - x.max().date()
                ).days
            ),
            frequency=(
                "transaction_date",
                "count"
            ),
            monetary=(
                "amount",
                "sum"
            ),
        )
    )

    return rfm

def safe_qcut(series, reverse=False):
    """
    Assign quantile-based scores while handling
    small datasets and duplicate values.
    """

    unique_values = series.nunique()

    if unique_values <= 1:
        return pd.Series(
            [3] * len(series),
            index=series.index
        )

    bins = min(5, unique_values)

    if reverse:
        labels = list(range(bins, 0, -1))
    else:
        labels = list(range(1, bins + 1))

    ranked = series.rank(method="first")

    return (
        pd.qcut(
            ranked,
            q=bins,
            labels=labels
        )
        .astype(int)
    )

def add_rfm_scores(rfm_df):

    if rfm_df.empty:
        return rfm_df

    rfm_df["r_score"] = safe_qcut(
        rfm_df["recency"],
        reverse=True
    )

    rfm_df["f_score"] = safe_qcut(
        rfm_df["frequency"]
    )

    rfm_df["m_score"] = safe_qcut(
        rfm_df["monetary"]
    )

    rfm_df["rfm_score"] = (

        rfm_df["r_score"]

        + rfm_df["f_score"]

        + rfm_df["m_score"]

    )

    return rfm_df