import sys
import os
import time

from src.anomaly_detection import detect_anomalies

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_processing import process_data
from src.risk_model import calculate_risk

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Financial Risk Analyst",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f8fafc 0%,
        #e0e7ff 50%,
        #dbeafe 100%
    );
}

/* Main headers */
h1 {
    color: #1e3a8a !important;
    font-size: 3rem !important;
}

h2,h3 {
    color: #1e40af !important;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0px 8px 24px rgba(0,0,0,0.08);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff,
        #eef2ff
    );
}

/* Dataframes */
.stDataFrame {
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 3rem;
    border-radius: 12px;
    border: none;
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    font-weight: bold;
}

/* Info Cards */
[data-testid="stAlert"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

st.markdown("""
# 🧠 AI Financial Risk Analyst

### Detect • Analyze • Explain Financial Risk
""")

st.caption(
    "AI-powered fraud detection and customer risk analysis platform"
)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## ⚙️ Controls")

    file = st.file_uploader(
        "Upload Dataset",
        type=["csv"],
        key="file1"
    )

    risk_filter = st.selectbox(
        "Risk Level",
        ["All", "High", "Medium", "Low"]
    )

    analyze = st.button(
        "🚀 Run Risk Analysis",
        use_container_width=True
    )

# ==================================================
# WAITING SCREEN
# ==================================================

if not file:

    st.info("""
### 👋 Welcome

Upload a financial transaction dataset from the sidebar and click:

🚀 **Run Risk Analysis**

The system will:

- Detect risky customers
- Identify suspicious transactions
- Generate risk insights
- Provide investigation recommendations
""")

# ==================================================
# MAIN ANALYSIS
# ==================================================

if file and analyze:

    progress = st.progress(0)

    with st.spinner(
        "🤖 AI is analyzing transaction patterns..."
    ):

        progress.progress(20)

        df = pd.read_csv(file)

        progress.progress(40)

        df, customer_df = process_data(df)

        progress.progress(70)

        customer_df = calculate_risk(customer_df)

        customer_df = detect_anomalies(customer_df)

        progress.progress(100)

        time.sleep(1)

    st.success("✅ Analysis Completed Successfully")

    # ==========================================
    # SUMMARY STATS
    # ==========================================

    high_risk = (
        customer_df["risk_label"] == "High"
    ).sum()

    medium_risk = (
        customer_df["risk_label"] == "Medium"
    ).sum()

    low_risk = (
        customer_df["risk_label"] == "Low"
    ).sum()

    # ==========================================
    # TABS
    # ==========================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 Executive Summary",
        "📊 Risk Analytics",
        "👥 Customer Explorer",
        "🚨 Suspicious Activity"
    ])

    # ==========================================
    # TAB 1 - SUMMARY
    # ==========================================

    with tab1:

        st.markdown("## 🤖 AI Executive Summary")

        st.info(f"""
### Key Findings

• High Risk Customers Identified: **{high_risk}**

• Medium Risk Customers Identified: **{medium_risk}**

• Average Risk Score: **{round(customer_df['risk_score'].mean(), 2)}**

• Highest Risk Score: **{customer_df['risk_score'].max()}**

• Total Customers Analyzed: **{len(customer_df)}**
""")

        st.markdown("### 📊 Portfolio Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Customers",
            f"{len(customer_df):,}"
        )

        c2.metric(
            "High Risk",
            f"{high_risk:,}"
        )

        c3.metric(
            "Medium Risk",
            f"{medium_risk:,}"
        )

        c4.metric(
            "Avg Risk Score",
            round(
                customer_df["risk_score"].mean(),
                2
            )
        )


        anomaly_count = (
            customer_df["anomaly"] == -1
        ).sum()

        st.success(f"""
        ### 🤖 AI Findings

        • {high_risk} High Risk Customers

        • {anomaly_count} Anomalous Customers

        • Transfer-heavy behavior is the dominant risk factor

        • Investigation Priority: HIGH
        """)

        st.success(f"""
### 🎯 Recommended Actions

1. Review the top {high_risk} high-risk customers

2. Investigate unusually large transfer transactions

3. Monitor customers with repeated suspicious activity

4. Prioritize accounts with previous fraud indicators

5. Escalate high-risk cases for manual review
""")

    # ==========================================
    # TAB 2 - ANALYTICS
    # ==========================================

    with tab2:

        st.markdown("## 📊 Risk Analytics")

        col1, col2 = st.columns(2)

        # Risk Distribution Pie Chart

        risk_counts = (
            customer_df["risk_label"]
            .value_counts()
        )

        fig1 = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Distribution",
            color=risk_counts.index,
            color_discrete_map={
                "High": "#ef4444",
                "Medium": "#f59e0b",
                "Low": "#22c55e"
            }
        )

        fig1.update_layout(
            height=500
        )

        col1.plotly_chart(
            fig1,
            use_container_width=True
        )

        # Avg Transaction Chart

        sample_chart = (
            customer_df
            .sort_values(
                "avg_amount",
                ascending=False
            )
            .head(20)
        )

        fig2 = px.bar(
            sample_chart,
            x=sample_chart.index,
            y="avg_amount",
            title="Top 20 Avg Transaction Amounts"
        )

        fig2.update_layout(
            height=500,
            xaxis_title="Customer",
            yaxis_title="Average Amount"
        )

        col2.plotly_chart(
            fig2,
            use_container_width=True
        )

        timeline = (
            df.groupby("step")["amount"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            timeline,
            x="step",
            y="amount",
            title="Transaction Volume Over Time"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ==========================================
    # TAB 3 - CUSTOMERS
    # ==========================================

    with tab3:

        st.markdown("## 👥 Customer Explorer")

        search = st.text_input(
            "🔍 Search Customer ID"
        )

        if search:

            search_results = customer_df[
                customer_df.index.astype(str)
                .str.contains(
                    search,
                    case=False
                )
            ]

            st.dataframe(
                search_results,
                use_container_width=True
            )

        if risk_filter != "All":

            filtered_df = customer_df[
                customer_df["risk_label"]
                == risk_filter
            ]

        else:

            filtered_df = customer_df

        st.markdown("### 🚨 Anomaly Detection")
        anomalies = customer_df[
            customer_df["anomaly"] == -1
        ]
        
        st.dataframe(
            anomalies.head(20),
            use_container_width=True
        )

        st.markdown("### 🔴 Top Risk Customers")

        top_users = (
            filtered_df
            .sort_values(
                by="risk_score",
                ascending=False
            )
            .head(20)
        )

        st.dataframe(
            top_users[
                [
                    "risk_score",
                    "risk_label",
                    "total_txn",
                    "avg_amount",
                    "transfer_ratio",
                    "reason"
                ]
            ],
            use_container_width=True
        )

        st.markdown("### 🔎 Customer Drill Down")

        selected_customer = st.selectbox(
            "Choose Customer",
            top_users.index.tolist()
        )

        if selected_customer:

            customer = customer_df.loc[
                selected_customer
            ]

            a, b, c = st.columns(3)

            a.metric(
                "Risk Score",
                customer["risk_score"]
            )

            b.metric(
                "Total Transactions",
                customer["total_txn"]
            )

            c.metric(
                "Avg Amount",
                round(
                    customer["avg_amount"],
                    2
                )
            )

            st.markdown("### Customer Profile")
            c1, c2, c3 = st.columns(3)
            
            c1.metric(
                "Transfer Ratio",
                round(customer["transfer_ratio"],2)
            )
            
            c2.metric(
                "Risk Label",
                customer["risk_label"]
            )
            
            c3.metric(
                "Fraud Count",
                customer["fraud_count"]
            )
            
            st.info(
                f"Reason: {customer['reason']}"
            )
    # ==========================================
    # TAB 4 - SUSPICIOUS ACTIVITY
    # ==========================================

    with tab4:

        st.markdown("## 🚨 Suspicious Transactions")

        amount_thresh = (
            df["amount"]
            .quantile(0.95)
        )

        suspicious = df[
            df["amount"] > amount_thresh
        ]

        st.metric(
            "Suspicious Transactions Found",
            len(suspicious)
        )

        st.dataframe(
            suspicious.head(100),
            use_container_width=True
        )

        st.caption(
            "Transactions above the 95th percentile are flagged as suspicious."
        )