# Remove duplicates after cleaning
# Runs after cleaning since dirty data could mask true duplicates
# Duplicates are either: 
# duplicate Transaction ID, or a duplicate of a subset of 'unique identifiers'

import pandas as pd

def deduplicate(df):
    # hard coding unique identifiers for now
    unique_identifiers = ['Customer ID', 'Item', 'Price Per Unit', 'Quantity', 'Payment Method', 'Location', 'Transaction Date']
    
    # First drop duplicates based on Transaction ID
    deduped_id = df[~df.duplicated(subset=['Transaction ID'], keep='first')] # get df excluding duplicates
    rejected_id = df[df.duplicated(subset=['Transaction ID'], keep='first')].copy() # get actual duplicates
    rejected_id['Error Info'] = 'Duplicate primary key' # adding an error column

    # Then drop duplicates based on unique_identifiers
    deduped_all = deduped_id[~deduped_id.duplicated(subset=unique_identifiers, keep='first')]
    rejected_unique = deduped_id[deduped_id.duplicated(subset=unique_identifiers, keep='first')].copy() # get rows that were removed again
    rejected_unique['Error Info'] = 'Duplicate subset of unique identifiers'

    # the combination of both rejected records based on Transaction ID and the unique_identifiers
    rejected_all = pd.concat([rejected_id, rejected_unique], ignore_index=True)

    return deduped_all, rejected_all