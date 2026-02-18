#perform feature engineering on transaction data to prepare it for analysis
#It adds new calculated columns, extracts time-based features, and computes customer lifetime value.

import pandas as pd

def add_features(df):

    # Revenue feature
    df["calculated_total"] = df["quantity"] * df["price"]
    df["price_difference"] = df["total_spent"] - df["calculated_total"] # Potentially see discount amount to use with has_discount column

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Time features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period('M')
    df["day_of_week"] = df["date"].dt.day_name()
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

    return df
