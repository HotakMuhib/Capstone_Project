from src.analysis.feature_engineering import add_features
from src.analysis.visualization import (
    plot_monthly_sales,
    plot_payment_method_distribution,
    plot_sales_by_location,
    plot_weekend_vs_weekday_sales,
    plot_sales_by_day_of_week,
    plot_top_categories,
    plot_lifetime_customer_value
)
from src.database.connection import get_connection
from sqlalchemy.sql import text
import pandas as pd

# -------------------- ANALYSIS --------------------
# After running the pipeline, we can perform some analysis on our data here
# We will query data from the database in order to do this

# First, get the data from the database and put it into a dataframe for later use in plotting
df = None
with get_connection() as conn:
    rs = conn.execute(text("SELECT * FROM transactions, items WHERE transactions.item_id = items.item_id"))
    rows = rs.fetchall()
    columns = rs.keys()
    df = pd.DataFrame(rows, columns=columns)

df.info()
# Feature engineer some useful features in feature_engineer.py
feature_df = add_features(df)

# Visualizations - main graphs
plot_monthly_sales(feature_df)
plot_top_categories(feature_df)
plot_sales_by_day_of_week(feature_df)
plot_payment_method_distribution(feature_df)

# Other graphs
#plot_sales_by_location(feature_df)
#plot_weekend_vs_weekday_sales(feature_df)
#plot_lifetime_customer_value(feature_df)