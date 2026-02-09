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

import logging
import os

#Logging setup
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/ingestion.log"),
        logging.FileHandler("logs/error.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ---------- READ ----------
retail_df = read_csv('./data/retail_store_sales.csv')
print(retail_df.info())
print(retail_df.head())
print(retail_df.isnull().sum()) # This data is dirty so we can clean it

logger.info("Null counts:\n%s", retail_df.isnull().sum())


# ---------- VALIDATE ----------
accepted, rejected = validate(retail_df)
print('Validation:')
print('Accepted Rows:', len(accepted))
print('Rejected Rows:', len(rejected))
validated_df = pd.DataFrame(accepted)
rejected_val = pd.DataFrame(rejected)

logger.info("Accepted rows: %d", len(accepted))
logger.warning("Rejected rows: %d", len(rejected))


# ---------- CLEAN ----------
clean_df = clean_data(validated_df)
logger.info("Data cleaning completed")

# ---------- DEDUPLICATE ----------
deduped_df, rejected_dedup = deduplicate(clean_df)
rejected_df = pd.concat([rejected_val, rejected_dedup])

logger.info("Deduplication completed: %d final rows", len(deduped_df))

print(deduped_df.info())
print(rejected_df.info())
print(rejected_df['Error Info'].unique())
