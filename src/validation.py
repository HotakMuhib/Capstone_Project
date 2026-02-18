# Validate and check the data AFTER reading from the .csv file and BEFORE cleaning
# for each row, we want to determine if the data is usable
#   - all required fields exist
#   - all data types are what we expect them to be
#   - any constraints specified in schema.yaml
# also add an Error Info col for the rejected rows to store reason for rejection

import pandas as pd
import yaml
import re

def validate(df):
    accepted = []
    rejected = []

    # We could later add .yaml filepath as an argument to validate function so that it can validate by multiple schemas
    with open('./config/schema.yaml', 'r') as file:
        schema = yaml.safe_load(file)

    required_fields = schema['validation_rules']['required_fields']
    field_types = schema['validation_rules']['field_types']
    constraints = schema['validation_rules']['constraints']

    # First checking if data contains all required columns
    missing_cols = [col for col in required_fields if col not in df.columns]
    if missing_cols:
        # If missing required columns, do not continue using this data
        raise Exception("File is missing required columns:", missing_cols)
    
    # Now checking each row
    for index, row in df.iterrows():
        errors = [] # put meaningful error messages in here

        # Check that required columns have existing values
        for required_field in required_fields:
            if pd.isna(row[required_field]):
                errors.append(f'Missing or null value in column: {required_field}')

        # Check that all fields match their expected data type
        if not errors:
            for field, required_type in field_types.items():
                val_in_row = row[field]
                try:
                    val_in_row = cast(val_in_row, required_type)
                except Exception:
                    errors.append(f'Value in {field} is not type: {required_type}')
        
        # Check all constraints
        # Add another if statement to add more constraints 
        if not errors:
            for field, constraint_dict in constraints.items():
                val_in_row = row[field]
                if 'min' in constraint_dict:
                    if val_in_row < constraint_dict['min']:
                        errors.append(f'Value in {field} is less than minimum: {constraint_dict["min"]}')
                if 'like' in constraint_dict:
                    if not re.search(str(constraint_dict['like']), str(val_in_row)):
                        errors.append(f'Value in {field} is not in an acceptable format')
                if 'in' in constraint_dict:
                    if val_in_row.lower() not in constraint_dict['in']:
                        errors.append(f'Value in {field} is not an acceptable predefined value')
        # Finally accept or reject the row
        if errors:
            row['Error Info'] = errors[0]
            rejected.append(row)
            errors = []
        else:
            accepted.append(row)

    return pd.DataFrame(accepted), pd.DataFrame(rejected)

def cast(var, type):
    if type == 'str':
        return str(var)
    elif type == 'int':
        return int(var)
    elif type == 'float':
        return float(var)
    elif type == 'bool':
        return bool(var)
    elif type == 'date':
        return pd.to_datetime(var)
    else:
        raise ValueError("Unexpected data type passed in")
