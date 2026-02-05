# Validate and check the data AFTER reading from the .csv file and BEFORE cleaning
# for each row, we want to determine if the data is usable
#   - all required fields exist
#   - all data types are what we expect them to be
#   - anything else to make sure the data makes sense

import pandas as pd
import yaml

def validate(df):
    accepted = []
    rejected = []

    # We could later add .yaml filepath as an argument to validate function so that it can validate by multiple schemas
    file = open('./config/schema.yaml', 'r')
    schema = yaml.safe_load(file)

    required_fields = schema['validation_rules']['required_fields']
    field_types = schema['validation_rules']['field_types']
    constraints = schema['validation_rules']['constraints']

    # First checking if data contains all required columns
    missing_cols = [col for col in required_fields if col not in df.columns]
    if missing_cols:
        # If missing required columns, do not continue using this data
        raise Exception("File is missing required columns:", missing_cols)
    
    # Log if there are any extra columns, but allow the data to pass
    extra_cols = [col for col in df.columns if col not in required_fields]
    if extra_cols:
        # Have logger write warning
        pass

    # Now checking each row
    for index, row in df.iterrows():
        errors = [] # put meaningful error messages in here

        # Check that required columns have existing values
        for required_field in required_fields:
            if pd.isna(row[required_field]):
                errors.append(f'Missing or null value in column: {required_field}')

        # Check that all fields match their expected data type
        for field, required_type in field_types.items():
            val_in_row = row[field]
            try:
                val_in_row = cast(val_in_row, required_type)
            except Exception:
                errors.append(f'Value in {field} is not type: {required_type}')
        
        # Check all constraints
        # Add another if statement to add more constraints 
        for field, constraint_dict in constraints.items():
            val_in_row = row[field]
            if 'min' in constraint_dict:
                if val_in_row < constraint_dict['min']:
                    errors.append(f'Value in {field} is less than minimum: {constraint_dict["min"]}')

        # Finally accept or reject the row
        if errors:
            rejected.append(row)
            errors = []
        else:
            accepted.append(row)

    return accepted, rejected

def cast(var, type):
    if type == 'str':
        str(var)
    elif type == 'int':
        int(var)
    elif type == 'float':
        float(var)
    elif type == 'bool':
        bool(var)
    else:
        raise ValueError("Unexpected data type passed in")