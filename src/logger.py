# write logs to /logs
# might add an extra error.log file if it feels like we should 
# split success and failure logs into two separate logs

import logging
from validation import validate

logging.basicConfig(
    filename="ingestion.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
accepted, rejected = validate
logging.info(f"Accepted rows: {len(accepted)}")
logging.warning(f"Rejected rows: {len(rejected)}")