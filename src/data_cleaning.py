# runs after validation
# standardize data by
#   - fill missing values with defaults for the rows that pass validation
#   - format and normalize text
#   - standardize date formats

import pandas as pd
import yaml

def clean_data(df):
    clean_df = df.copy()

    with open('./config/schema.yaml', 'r') as file:
        schema = yaml.safe_load(file)
    
    field_types = schema['validation_rules']['field_types']

    for field, required_type in field_types.items():
        if required_type == 'str':
            pass
        elif required_type == 'int' or required_type == 'float':
            clean_df[field] = pd.to_numeric(df[field])
        elif required_type == 'bool':
            clean_df[field] = [x in (True, 'True', 'true', 1, '1', 'Yes', 'yes') for x in df[field]]
        elif required_type == 'date':
            clean_df[field] = pd.to_datetime(df[field], format='mixed')
    
    return clean_df