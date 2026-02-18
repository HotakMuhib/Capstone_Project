# This is the pipeline driver
# it will run all the necesssary files from here
# PIPELINE FLOW:
# Ingest -> Validate -> Clean -> Deduplicate -> Load 

# CODE FLOW:
# import from our directories
# set up logger, then run:
# csv_reader.py -> validation.py -> data_cleaning.py -> deduplication.py -> connection.py + loader.py 

import pandas as pd
import logging
import os
from src.validation import validate
from src.data_cleaning import clean_data
from src.deduplication import deduplicate
from src.ingestion.csv_json_reader import read_source
from src.config_loader import load_yaml
from src.database.connection import get_connection
from src.database.init_db import create_tables, drop_tables
from src.database.loader import load_accepted_records, load_rejected_records

# Logging setup
os.makedirs("logs", exist_ok=True) # create a log directory,

logging.basicConfig(             # configure logging output
    level=logging.INFO,          # log info, warning, error critical
    format="%(asctime)s %(levelname)s %(message)s",  
    handlers=[                  # where log goes
        logging.FileHandler("logs/ingestion.log", mode="w"),
        logging.StreamHandler()        #  print log to the terminal while script runs
    ]
)

logger = logging.getLogger(__name__)    # create or retrieve logger name after module

####################     BEGIN PIPELINE     ####################

logger.info("Pipeline is beginning execution")
# -------------------- INGEST --------------------

# Load YAML
sources = load_yaml("config/sources.yaml")
# Select the source
sales_config = sources["sales_csv"]
# Read dynamically
retail_df = read_source(sales_config)
logger.info("Ingestion done. Filepaths are correct.") 


# -------------------- VALIDATE --------------------
validated_df, rejected_val = validate(retail_df)

# Log the total accepted rows
logger.info("Validation completed: %d final rows", len(validated_df))
# Log how many rows failed validation
logger.warning("Rejected rows from Validation: %d", len(rejected_val))

# -------------------- CLEAN --------------------
clean_df = clean_data(validated_df)
logger.info("Data cleaning completed")

# -------------------- DEDUPLICATE --------------------
deduped_df, rejected_dedup = deduplicate(clean_df)
rejected_df = pd.concat([rejected_val, rejected_dedup])

logger.info("Deduplication completed: %d final rows", len(deduped_df))
logger.warning("Rejected rows from Deduplication: %d", len(rejected_df) - len(rejected_val))

print(deduped_df.info())
print(rejected_df['Error Info'].unique())

print(deduped_df.head())
rejected_df.info()

# -------------------- LOAD --------------------
with get_connection() as conn:
    logger.info("Successfully connected to database")
    drop_tables(conn)
    create_tables(conn)
    logger.info("Created tables in database. Ready for loading")
    load_accepted_records(deduped_df, conn)
    load_rejected_records(rejected_df, conn)
    conn.commit()
    logger.info("Loaded into database")

logger.info("Pipeline has finished execution")
