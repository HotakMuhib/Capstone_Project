# runs after validation
# standardize data by
#   - fill missing values with defaults for the rows that pass validation
#   - format and normalize text
#   - standardize date formats

import pandas as pd
import yaml
import re

def clean_data(df):
    clean_df = df.copy()

    with open('./config/schema.yaml', 'r') as file:
        schema = yaml.safe_load(file)
    
    field_types = schema['validation_rules']['field_types']
    string_cleaning_formats = schema['string_cleaning_formats']

    for field, required_type in field_types.items():
        # for string cols, strip leading and trailing whitespace then use config rules
        if required_type == 'str':
            df[field] = df[field].str.strip()
            for key in string_cleaning_formats:
                if field in string_cleaning_formats[key]['columns']:
                    if key == 'title case':
                        clean_df[field] = df[field].str.title()
                    elif key == 'id_format':
                        clean_df[field] = df[field].str.extract(str(string_cleaning_formats[key]['regex']))
                    elif key == 'item_format':
                        clean_df[field] = df[field].str.extract(str(string_cleaning_formats[key]['regex']))
        # for numeric cols, cast from string to numeric
        elif required_type == 'int' or required_type == 'float':
            clean_df[field] = pd.to_numeric(df[field])
        # for boolean cols, map True to a set of possible truthy values
        elif required_type == 'bool':
            clean_df[field] = [x in (True, 'True', 'true', 1, '1', 'Yes', 'yes') for x in df[field]]
        # for date cols, standardize date format and convert to datetime
        elif required_type == 'date':
            clean_df[field] = pd.to_datetime(df[field], format='mixed')
    
    return clean_df