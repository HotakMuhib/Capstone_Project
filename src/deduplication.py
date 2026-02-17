# Remove duplicates after cleaning
# Why after cleaning? Since dirty data could mask true duplicates
# We could delete duplicates based on Transaction ID 
# and a combination of other cols that if another row has the same values in these cols, it is very likely a duplicate entry
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