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
from validation import validate
from data_cleaning import clean_data
from deduplication import deduplicate
from ingestion.csv_json_reader import read_source

from config_loader import load_yaml


import logging
import os

#Logging setup
os.makedirs("logs", exist_ok=True) #create a log directory,

logging.basicConfig(             #configure logging outp
    level=logging.INFO,          #log info, warning, error critical
    format="%(asctime)s %(levelname)s %(message)s",  
    handlers=[                  #where log goes
        logging.FileHandler("logs/ingestion.log"),
        logging.FileHandler("logs/error.log"),
        logging.StreamHandler()        #.  print log to the terminal while script runs
    ]
)

logger = logging.getLogger(__name__)    #create or retrieve logger name after module


# ---------- READ ----------
# retail_df = read_csv('./data/retail_store_sales.csv') 

# Load YAML
sources = load_yaml("config/sources.yaml")

# Select the source
sales_config = sources["sales_csv"]

# Read dynamically
retail_df = read_source(sales_config) 

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
