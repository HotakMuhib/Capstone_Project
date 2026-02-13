# # INSERT data into the tables in our database here
# # Should use parameterized queries in Python

# def load_dataframe(df, table_name, engine):
#     df.to_sql(
#         table_name,
#         engine,
#         if_exists="append",
#         index=False
#     )