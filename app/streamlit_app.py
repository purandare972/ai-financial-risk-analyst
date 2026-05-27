import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from src.data_processing import process_data
from src.risk_model import calculate_risk

st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    /* Cards / containers */
    .css-1d391kg {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 10px;
    }

    /* Headers */
    h1, h2, h3 {
        color: #38bdf8;
    }

    /* Metric boxes */
    [data-testid="metric-container"] {
        background-color: #020617;
        border: 1px solid #38bdf8;
        padding: 10px;
        border-radius: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #38bdf8;
        color: black;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# 🧠 AI Financial Risk Analyst  
### Detect • Analyze • Explain Financial Risk
""")

file = st.file_uploader("Upload dataset", key="file1")

if file:
    df = pd.read_csv(file)

    # Process
    df, customer_df = process_data(df)
    customer_df = calculate_risk(customer_df)

    # ------------------ OVERVIEW ------------------
    st.markdown("## 📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", len(customer_df))
    col2.metric("High Risk", (customer_df['risk_score'] > 70).sum())
    col3.metric("Avg Risk Score", round(customer_df['risk_score'].mean(), 2))

    st.markdown("---")

    # ------------------ FILTER ------------------
    st.markdown("## 🎯 Filter")

    risk_filter = st.selectbox(
        "Select Risk Level",
        ["All", "High", "Medium", "Low"]
    )

    if risk_filter != "All":
        filtered_df = customer_df[customer_df['risk_label'] == risk_filter]
    else:
        filtered_df = customer_df

    # ------------------ TOP USERS ------------------
    with st.container():
            st.markdown("## 🔴 Top Risky Customers")
            top_users = filtered_df.sort_values(by='risk_score', ascending=False).head(10)
            
            st.dataframe(
                top_users[['risk_score','total_txn','avg_amount','transfer_ratio','reason']],use_container_width=True
            )
            
            if len(top_users) > 0:
                 top = top_users.iloc[0]
                 st.warning(f"⚠️ Highest Risk User: {top.name} (Score: {top['risk_score']})")

    st.markdown("---")

    # ------------------ CHARTS ------------------
    st.markdown("## 📈 Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Risk Distribution")
        st.bar_chart(customer_df['risk_label'].value_counts())

    with col2:
        st.write("Transaction Behavior")
        st.bar_chart(customer_df['avg_amount'].head(50))

    st.markdown("---")

    # ------------------ SUSPICIOUS ------------------
    st.markdown("## 🚨 Suspicious Transactions")

    amount_thresh = df['amount'].quantile(0.95)
    suspicious = df[df['amount'] > amount_thresh]

    st.dataframe(suspicious.head(20), use_container_width=True)