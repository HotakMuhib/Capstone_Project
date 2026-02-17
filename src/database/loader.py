# # INSERT data into the tables in our database here
# # Should use parameterized queries in Python

def load_accepted_records(df, conn):
    if df.empty:
        return
    
    # Change all column names to match the database in preparation for insertion
    renaming = {'Transaction ID': 'transaction_id',
                'Customer ID': 'cust_id',
                'Category': 'category',
                'Item': 'item_id',
                'Price Per Unit': 'price',
                'Quantity': 'quantity',
                'Total Spent': 'total_spent',
                'Payment Method': 'method',
                'Location': 'location',
                'Transaction Date': 'date',
                'Discount Applied': 'has_discount'
                }
    df = df.rename(columns=renaming)

    # Initialize unique items then insert
    df_items = df[['category', 'item_id', 'price']]
    df_items = df_items.drop_duplicates(subset=['item_id'], keep='first', inplace=False)
    df_items.to_sql(
        name="items",
        con = conn,
        if_exists="append",
        index=False,
        method="multi"
    )

    # Insert transactions
    df_transactions = df[['transaction_id', 'cust_id', 'quantity', 'total_spent', 'method', 'location', 'date', 'has_discount']]
    df_transactions.to_sql(
        name="transactions",
        con=conn,
        if_exists="append",
        index=False,
        method="multi"
    )

def load_rejected_records(df, conn):
    if df.empty:
        return
    
    renaming = {'Transaction ID': 'transaction_id',
                'Customer ID': 'cust_id',
                'Category': 'category',
                'Item': 'item_id',
                'Price Per Unit': 'price',
                'Quantity': 'quantity',
                'Total Spent': 'total_spent',
                'Payment Method': 'method',
                'Location': 'location',
                'Transaction Date': 'date',
                'Discount Applied': 'has_discount',
                'Error Info': 'error_info'
                }
    df = df.rename(columns=renaming)

    df.to_sql(
        name="rejected_records",
        con=conn,
        if_exists="append",
        index=False,
        method="multi"
    )