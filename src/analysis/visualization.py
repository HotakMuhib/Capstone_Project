

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Groups transactions by month and sums Total Spent.
# Plots a line chart showing total revenue per month.
# Helps you see monthly sales trends.

def plot_monthly_sales(df):
    """Line chart of total monthly revenue."""
    monthly_sales = df.groupby("month")["Total Spent"].sum()
    monthly_sales.plot(marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue")
    plt.show()


# Counts how many transactions were made using each Payment Method.
# Plots a bar chart of transaction counts per payment type.
# Shows which payment methods are most popular.
def plot_payment_method_distribution(df):
    """Bar chart of payment method usage."""
    counts = df["Payment Method"].value_counts()
    counts.plot(kind="bar")
    plt.title("Payment Method Distribution")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")
    plt.show()


# Groups transactions by is_weekend (True/False) and sums Total Spent.
# Plots a bar chart comparing weekend vs weekday revenue.
# Shows whether more revenue comes from weekends or weekdays.
def plot_weekend_vs_weekday_sales(df):
    """Bar chart comparing weekend vs weekday revenue."""
    sales = df.groupby("is_weekend")["Total Spent"].sum()
    sales.plot(kind="bar")
    plt.title("Weekend vs Weekday Revenue")
    plt.xlabel("Is Weekend")
    plt.ylabel("Total Revenue")
    plt.show()

# Groups transactions by Item and sums Total Spent.
# Selects the top N items by revenue.
# Plots a bar chart of revenue for these top items.
# Shows which products generate the most sales.
def plot_top_items(df, top_n=10):
    """Bar chart of top N items by revenue."""
    top_items = df.groupby("Item")["Total Spent"].sum().sort_values(ascending=False).head(top_n)
    top_items.plot(kind="bar")
    plt.title(f"Top {top_n} Items by Revenue")
    plt.ylabel("Total Revenue")
    plt.show()
