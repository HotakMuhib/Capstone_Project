# Remove duplicates after cleaning
# Why after cleaning? Since dirty data could mask true duplicates
# We could delete duplicates based on Transaction ID 
# and a combination of other cols that if another row has the same values in these cols, it is very likely a duplicate entry

def deduplicate(df):
    # hard coding unique identifiers for now
    unique_identifiers = ['Customer ID', 'Item', 'Price Per Unit','Quantity', 'Payment Method', 'Location', 'Transaction Date']
    
    # First drop duplicates based on Transaction ID
    deduped_id = df.drop_duplicates(subset=['Transaction ID'], keep='first')
    # rejected_id = df - deduped_id # get rows that were removed from the original

    # Then drop duplicates based on unique_identifiers
    deduped_all = deduped_id.drop_duplicates(subset=unique_identifiers, keep='first')
    # rejected_unique = deduped_id - deduped_all # get rows that were removed again

    # the combination of both rejected records based on Transaction ID and the unique_identifiers
    # rejected_all = rejected_id + rejected_unique

    return deduped_all #, rejected_all