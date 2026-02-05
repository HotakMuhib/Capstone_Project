# This is the pipeline driver
# it will run all the necesssary files from here
#
# Ingest -> Validate -> Clean -> Load -> Log -> Test



# CODE FLOW:
# import from our directories
# set up logger, then run:
# csv_reader.py -> validation.py -> data_cleaning.py -> connection.py + loader.py -> logger.py -> tests/
# 
# 
#


# CURRENTLY, main.py WILL BE USED FOR TESTING EARLY CODE AND DOING SOME EXPLORATORY ANALYSIS ON THE DATA

from ingestion.csv_reader import read_csv
from validation import validate

# # Show some info on our dataset
# chocolate_df = read_csv('.\data\Chocolate Sales.csv')
# print(chocolate_df.info())
# print(chocolate_df.head())
# print(chocolate_df.isnull().sum()) # Print the number of Null values in each column
# # this data is already clean

# print('--------------------------------')

# # Show some info on another potential dataset
# chocolate2_df = read_csv('./data/chocolate_sales2.csv')
# print(chocolate2_df.info())
# print(chocolate2_df.head())
# print(chocolate2_df.isnull().sum()) 

# print('--------------------------------')

# Show some info on another potential dataset
retail_df = read_csv('./data/retail_store_sales.csv')
print(retail_df.info())
print(retail_df.head())
print(retail_df.isnull().sum()) # This data is dirty so we can clean it

accepted, rejected = validate(retail_df)
print(len(accepted))
print(len(rejected))