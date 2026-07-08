# Customer Segmentation Module

## Overview

The Customer Segmentation module is the first Machine Learning component of the **CustomerSphere AI – Multi-Tenant Customer Intelligence Platform for SMEs**.

Its purpose is to automatically group customers into meaningful business segments based on their purchasing behavior using **RFM Analysis (Recency, Frequency, Monetary)** and the **K-Means Clustering** algorithm.

The generated segments help organizations identify valuable customers, understand customer behavior, and support business decisions such as customer retention, marketing campaigns, loyalty programs, and future AI-based recommendations.

---

Objectives

* Generate customer RFM features from transactional data.
* Prepare data for machine learning using feature scaling.
* Train a K-Means clustering model.
* Predict customer segments.
* Convert technical cluster IDs into business-friendly customer segments.
* Maintain complete tenant isolation so each organization trains and predicts only on its own customer data.

---

Machine Learning Workflow

```text
PostgreSQL
      │
      ▼
SegmentationRepository
      │
      ▼
Feature Engineering
      │
      ▼
RFM Dataset
      │
      ▼
RFM Scoring
      │
      ▼
StandardScaler
      │
      ▼
K-Means Training
      │
      ▼
Business Segment Mapping
      │
      ▼
Prediction API
```

---

RFM Analysis

The module calculates three important customer behavior metrics.

Recency (R)

Number of days since the customer's most recent purchase.

Lower values indicate a more recently active customer.

---

Frequency (F)

Total number of completed purchases made by a customer.

Higher values indicate a more loyal customer.

---

Monetary (M)

Total amount spent by the customer.

Higher values indicate higher customer value.

---

RFM Scoring

Each metric is converted into a score using quantile-based ranking.

| Metric    | Better Value |
| --------- | ------------ |
| Recency   | Lower        |
| Frequency | Higher       |
| Monetary  | Higher       |

The overall RFM Score is calculated as:

```text
RFM Score = R Score + F Score + M Score
```

---

Feature Scaling

Before clustering, the RFM features are standardized using **StandardScaler**.

Scaling ensures that:

* Monetary values do not dominate clustering.
* Distance calculations remain meaningful.
* K-Means performs correctly.

---

K-Means Clustering

The clustering model groups customers with similar purchasing behavior.

The implementation uses:

* K-Means
* Random State = 42
* StandardScaler
* Joblib model persistence

---

Elbow Method

During model training, the Elbow Method is executed to evaluate different cluster counts.

The resulting graph is stored for documentation and analysis.

Generated file:

```text
model_registry/
└── segmentation/
    └── elbow_curve.png
```

---

Business Segment Mapping

K-Means generates numeric cluster IDs.

Example:

```text
Cluster 0
Cluster 1
Cluster 2
```

Since cluster IDs have no business meaning and may change after retraining, they are converted into business-friendly labels.

Example:

* Champions
* Loyal Customers
* Big Spenders
* Potential Loyalists
* At Risk
* Lost Customers

The mapping is automatically generated after training and stored as:

```text
model_registry/
└── segmentation/
    └── label_mapping.json
```

---

Multi-Tenant Support

The module is fully multi-tenant.

Each organization:

* trains its own segmentation model,
* predicts only its own customers,
* cannot access another organization's data.

All database queries are filtered using the authenticated user's `org_id`.

---

Generated Files

After successful training, the following artifacts are generated.

```text
model_registry/

segmentation/

    scaler.pkl
    kmeans.pkl
    elbow_curve.png
    label_mapping.json
```

Optional training dataset:

```text
data/

training/

    rfm_dataset.csv
```

---

API Endpoints

Train Model

```http
POST /segmentation/train
```

Purpose:

* Generate RFM dataset
* Scale features
* Train K-Means
* Save scaler
* Save model
* Generate elbow plot
* Generate business segment mapping

---

Predict Customer Segments

```http
GET /segmentation/predict
```

Purpose:

* Load saved scaler
* Load trained model
* Generate fresh RFM data
* Predict customer clusters
* Return business-friendly customer segments

---

Folder Structure

```text
backend/

ml/

segmentation/

    dataset.py
    feature_engineering.py
    preprocessing.py
    clustering.py
    train.py
    predict.py
    utils.py
```

---

Technologies Used

* Python
* Pandas
* Scikit-Learn
* SQLAlchemy
* PostgreSQL
* Joblib
* FastAPI

---

Future Enhancements

The segmentation pipeline is designed to support future modules including:

* Churn Prediction
* Customer Lifetime Value Prediction
* Next Purchase Prediction
* AI Business Insights
* Personalized Recommendations

The reusable preprocessing and feature engineering pipeline minimizes duplicate code across future machine learning modules.

---

Summary

The Customer Segmentation module provides an automated, production-inspired customer intelligence pipeline for SMEs. It combines transactional data, RFM analysis, feature engineering, clustering, and business-oriented interpretation to produce actionable customer segments while maintaining a clean Repository-Service architecture and complete multi-tenant isolation.
