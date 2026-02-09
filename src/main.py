# This is the pipeline driver
# it will run all the necesssary files from here
#
# Ingest -> Validate -> Clean -> Deduplication -> Load -> Log -> Test



# CODE FLOW:
# import from our directories
# set up logger, then run:
# csv_reader.py -> validation.py -> data_cleaning.py -> deduplication.py -> connection.py + loader.py -> logger.py -> tests/
# 
# 
#
import pandas as pd
from ingestion.csv_reader import read_csv
from validation import validate
from data_cleaning import clean_data
from deduplication import deduplicate



# ---------- READ ----------
retail_df = read_csv('./data/retail_store_sales.csv')
print(retail_df.info())
print(retail_df.head())
print(retail_df.isnull().sum()) # This data is dirty so we can clean it

# ---------- VALIDATE ----------
accepted, rejected = validate(retail_df)
print('Validation:')
print('Accepted Rows:', len(accepted))
print('Rejected Rows:', len(rejected))
validated_df = pd.DataFrame(accepted)

# ---------- CLEAN ----------
clean_df = clean_data(validated_df)

# ---------- DEDUPLICATE ----------
deduped_df, rejected_df = deduplicate(clean_df)

print(deduped_df.info())
print(rejected_df.head())