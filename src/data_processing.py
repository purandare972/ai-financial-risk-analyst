import pandas as pd

def process_data(df):

    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # select correct columns
    df = df[['step','type','amount','nameorig','isfraud']]

    # clean data
    df = df.dropna().drop_duplicates()

    # IMPORTANT: handle type values properly
    df['type'] = df['type'].str.upper()

    # feature creation
    df['is_transfer'] = (df['type'] == 'TRANSFER').astype(int)

    # aggregation
    customer_df = df.groupby('nameorig').agg({
        'amount': ['count','mean','max','sum'],
        'isfraud': 'sum',
        'is_transfer': 'mean'
    })

    # rename columns
    customer_df.columns = [
        'total_txn','avg_amount','max_amount','total_amount',
        'fraud_count','transfer_ratio'
    ]

    return df, customer_df