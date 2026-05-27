import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import pandas as pd
from src.data_processing import process_data
from src.risk_model import calculate_risk

st.title("AI Financial Risk Analyst")

file = st.file_uploader("Upload dataset")

if file:
    df = pd.read_csv(file)

    st.write(df.head())
    st.write("Columns in dataset:", df.columns.tolist())

    # Create customer_df first
    df, customer_df = process_data(df)
    customer_df = calculate_risk(customer_df)

    st.subheader("Top Risk Customers")
    st.dataframe(
        customer_df.sort_values(by='risk_score', ascending=False)
        [['risk_score', 'total_txn', 'avg_amount', 'transfer_ratio', 'reason']]
        .head(10)
    )

    st.subheader("Risk Distribution")
    st.bar_chart(customer_df['risk_score'].value_counts())