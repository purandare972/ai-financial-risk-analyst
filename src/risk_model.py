def calculate_risk(customer_df):

    amount_thresh = customer_df['avg_amount'].quantile(0.95)
    txn_thresh = customer_df['total_txn'].quantile(0.90)

    def risk_score(row):
        score = 0
        if row['avg_amount'] > amount_thresh:
            score += 30
        if row['total_txn'] > txn_thresh:
            score += 20
        if row['transfer_ratio'] > 0.6:
            score += 30
        if row['fraud_count'] > 0:
            score += 50
        return score

    customer_df['risk_score'] = customer_df.apply(risk_score, axis=1)

    # ✅ ADD THIS BLOCK (VERY IMPORTANT)
    def label(score):
        if score > 70:
            return 'High'
        elif score > 30:
            return 'Medium'
        else:
            return 'Low'

    customer_df['risk_label'] = customer_df['risk_score'].apply(label)

    # ---------------- EXPLANATION ----------------
    def explain(row):
        reasons = []

        if row['avg_amount'] > amount_thresh:
            reasons.append("High avg transaction")

        if row['total_txn'] > txn_thresh:
            reasons.append("High transaction count")

        if row['transfer_ratio'] > 0.6:
            reasons.append("High transfer activity")

        if row['fraud_count'] > 0:
            reasons.append("Past fraud detected")

        if not reasons:
            reasons.append("Low risk")

        return ", ".join(reasons)

    customer_df['reason'] = customer_df.apply(explain, axis=1)

    return customer_df