import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
from src.database.connection import get_connection
from sqlalchemy.sql import text


plt.style.use("ggplot")
plt.rcParams.update({
    "figure.figsize": (16, 8),
    "figure.dpi": 110,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11
})


# Groups transactions by month and sums Total Spent.
# Plots a line chart showing total revenue per month.
# Helps you see monthly sales trends.

def plot_monthly_sales(df):
    """Line chart of total monthly revenue."""
    monthly_sales = df.groupby("month")["total_spent"].sum()

    plt.figure()
    monthly_sales.plot( marker="o", color="magenta")
    plt.title("All-time Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue ($)")
    plt.xticks(rotation=45)
    plt.grid(which="major", color="black", linewidth="0.5")
    plt.grid(which="minor", color="gray", linewidth="0.3")
    plt.show()

# Counts how many transactions were made using each Payment Method.
# Plots a pie chart of transaction counts per payment type.
# Shows which payment methods are most popular.
def plot_payment_method_distribution(df):
    """Pie chart of payment method usage."""
    counts = df["method"].value_counts()
    wedges, texts, autotexts = plt.pie(counts.values, autopct="%1.1f%%", startangle=90, wedgeprops={"edgecolor": "white"})
    plt.title("Payment Method Distribution")
    plt.legend(wedges, counts.index, title="Payment Method", loc="lower left")

    # Increase % label size
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_weight("bold")
    plt.show()

# Groups transactions by Location and sums Total Spent.
# Plots a bar chart showing the total revenue of each location type
def plot_sales_by_location(df):
    """Bar chart of online vs in-store sales."""
    location_sales = df.groupby("location")["total_spent"].sum()
    location_sales.plot(kind="bar")
    plt.title("Sales by Location")
    plt.ylabel("Total Revenue")
    plt.show()

# Groups transactions by is_weekend (True/False) and sums Total Spent.
# Plots a bar chart comparing weekend vs weekday revenue.
# Shows whether more revenue comes from weekends or weekdays.
def plot_weekend_vs_weekday_sales(df):
    """Bar chart comparing weekend vs weekday revenue."""
    sales = df.groupby("is_weekend")["total_spent"].sum()
    bars = plt.bar(sales.index, sales.values)
    plt.title("Weekend vs Weekday Revenue")
    plt.xlabel("Is Weekend")
    plt.ylabel("Total Revenue")

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height} $",
            ha="center",
            va="bottom")
    plt.show()

# Similar to previous plot, this one will compare sales between each individual day
def plot_sales_by_day_of_week(df):
    """Bar chart comparing each day of the week."""
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sales = df.groupby("day_of_week")["total_spent"].sum().reindex(day_order)
    bars = plt.bar(sales.index, sales.values, color="cadetblue")
    plt.title("Revenue by Day")
    plt.xlabel("Day")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=30)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height} $",
            ha="center",
            va="bottom")
    plt.show()

# Groups transactions by Category and sums Total Spent.
# Selects the top N items by revenue.
# Plots a bar chart of revenue for these top items.
# Shows which products generate the most sales.
def plot_top_categories(df, top_n=10):
    """Bar chart of top N items by revenue."""
    category_sales = df.groupby("category")["total_spent"].sum().sort_values(ascending=False).head(top_n)
    bars = plt.bar(category_sales.index, category_sales.values, color="mediumseagreen")
    plt.title(f"Top {top_n} Item Categories by Revenue")
    plt.ylabel("Total Revenue ($)")
    plt.xticks(rotation=15)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height} $",
            ha="center",
            va="bottom")
    plt.show()

# Groups transactions by Customer ID and sums Total Spent.
# Selects the top N customers by revenue.
def plot_lifetime_customer_value(df, top_n=5):
    """Bar chart of top N customers by total spent over all transactions."""
    customer_lifetime_values = df.groupby("cust_id")["total_spent"].sum().sort_values(ascending=False).head(top_n)
    customer_lifetime_values.plot(kind="bar")
    plt.title(f"Top {top_n} Highest Spending Customers (All-time)")
    #plt.ylabel("Total Spent")
    plt.show()
