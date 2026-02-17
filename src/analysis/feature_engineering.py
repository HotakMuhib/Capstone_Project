#perform feature engineering on transaction data to prepare it for analysis
#It adds new calculated columns, extracts time-based features, and computes customer lifetime value.

# analysis/feature_engineering.py

import pandas as pd

def add_features(df):

    # Revenue feature
    df["calculated_total"] = df["Quantity"] * df["Price Per Unit"]
    df["price_difference"] = df["Total Spent"] - df["calculated_total"]

    # Convert date column
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

    # Time features
    df["year"] = df["Transaction Date"].dt.year
    df["month"] = df["Transaction Date"].dt.month
    df["day_of_week"] = df["Transaction Date"].dt.day_name()
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

    # Customer lifetime value
    df["lifetime_value"] = df.groupby("Customer ID")["Total Spent"].transform("sum")

    return df
