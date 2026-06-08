from sklearn.ensemble import IsolationForest

def detect_anomalies(customer_df):

    features = customer_df[
        ["avg_amount", "total_txn", "transfer_ratio"]
    ]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    customer_df["anomaly"] = model.fit_predict(features)

    return customer_df