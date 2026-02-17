from src.validation import validate, cast
import pandas as pd
import pytest

def test_missing_column_exception():
    ### Test that validation rejects data that is missing required columns
    bad_data = {"Transaction ID": ['TXN_6867343', 'TXN_3731986'],
                "Total Spent": ['14.0', '300.0'],
                "Discount Applied": [True, False]}
    missing_col_df = pd.DataFrame(bad_data)

    with pytest.raises(Exception) as ex:
        validate(missing_col_df)
    assert str(ex.value).startswith("File is missing required columns:", 2) # start at index 2 since it is where exception string begins

def test_null_in_required_col():
    ### Test that required columns are rejected if they have null values
    has_null_val = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": [None],               # Missing item
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_null_val)

    accepted, rejected = validate(df)
    
    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Missing or null value in column: Item"

def test_invalid_type_in_col():
    ### Test that a row is rejected if it has an improper data type
    has_invalid_type = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],       
                    "Price Per Unit": [14.0],
                    "Quantity": ['err'],        # list instead of int; non cast-able
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_invalid_type)

    accepted, rejected = validate(df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Value in Quantity is not type: int"

def test_fail_constraint_min():
    ### Test that a row is rejected if it fails a 'min' constraint
    has_neg_price = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],       
                    "Price Per Unit": [-14.0],  # should not be less than 0
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_neg_price)

    accepted, rejected = validate(df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Value in Price Per Unit is less than minimum: 0"

def test_fail_constraint_like_id():
    ### Test that a row is rejected if it fails a 'like' constraint for transaction or customer id formats
    has_misformat_id = {"Transaction ID": ['TXN_6867343zxy'], # Must end with only numericals
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],       
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_misformat_id)

    accepted, rejected = validate(df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Value in Transaction ID is not in an acceptable format"

def test_fail_constraint_like_item():
    ### Test that a row is rejected if it fails a 'like' constraint for an item format
    has_misformat_item = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_1490PAT_'], # Not in 123_ABC format       
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_misformat_item)

    accepted, rejected = validate(df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Value in Item is not in an acceptable format"

def test_pass_constraint_like_id():
    ### Test that an altered id passes 'like' constraint
    has_okayformat_id = {"Transaction ID": ['_6867343'], # Valid since it ends with numericals
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],       
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_okayformat_id)

    accepted, rejected = validate(df)

    assert len(accepted) == 1
    assert len(rejected) == 0

def test_pass_constraint_like_item():
    ### Test that an altered item passes 'like' constraint
    has_okayformat_item = {"Transaction ID": ['_6867343'], 
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['10_PAT'],     # Matches 123-ABC
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['Credit Card'],
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_okayformat_item)

    accepted, rejected = validate(df)

    assert len(accepted) == 1
    assert len(rejected) == 0

def test_fail_constraint_in():
    ### Test that a row is rejected if it fails 'in' acceptable subset constraint
    has_invalid_method = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],      
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['something else'], # Not acceptable value
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_invalid_method)

    accepted, rejected = validate(df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert str(rejected.iloc[0]['Error Info']) == "Value in Payment Method is not an acceptable predefined value"

def test_pass_constraint_in():
    ### Test that 'in' constraint is case insensitive
    has_okay_method = {"Transaction ID": ['TXN_6867343'],
                    "Customer ID": ['CUST_12'],
                    "Category": ['Patisserie'],
                    "Item": ['Item_10_PAT'],      
                    "Price Per Unit": [14.0],
                    "Quantity": [2.0],        
                    "Total Spent": [28.0],
                    "Payment Method": ['credit card'], # Okay since check is case insensitive
                    "Location": ['In-Store'],
                    "Transaction Date": ['2022-10-05'],
                    "Discount Applied": [True]}
    df = pd.DataFrame(has_okay_method)

    accepted, rejected = validate(df)

    assert len(accepted) == 1
    assert len(rejected) == 0

def test_invalid_cast_type():
    ### Test that helper cast function throws an exception when an unexpected type is passed through
    var = 123
    type = "something else"

    with pytest.raises(Exception) as ex:
        cast(var, type)
    assert str(ex.value).startswith("Unexpected data type passed in")

def test_successful_validation():
    ### Test that a valid row makes it through validation
    data = {"Transaction ID": ['TXN_6867343'],
            "Customer ID": ['CUST_12'],
            "Category": ['Patisserie'],
            "Item": ['Item_10_PAT'],      
            "Price Per Unit": [14.0],
            "Quantity": [2.0],        
            "Total Spent": [28.0],
            "Payment Method": ['Credit Card'], 
            "Location": ['In-Store'],
            "Transaction Date": ['2022-10-05'],
            "Discount Applied": [True]}
    df = pd.DataFrame(data)

    accepted, rejected = validate(df)

    assert len(accepted) == 1
    assert len(rejected) == 0

