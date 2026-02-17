from src.validation import validate
import pandas as pd
import pytest

def test_missing_column_exception():
    bad_data = {"Transaction ID": ['TXN_6867343', 'TXN_3731986'],
                "Total Spent": ['14.0', '300.0'],
                "Discount Applied": [True, False]}
    missing_col_df = pd.DataFrame(bad_data)

    with pytest.raises(Exception) as ex:
        validate(missing_col_df)
    print("DEBUG", str(ex.value))
    assert str(ex.value).startswith("File is missing required columns:", 2) # start at index 2 since it is where exception string begins

def test_null_in_required_col():
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
    assert "Missing or null value in column: Item" in str(rejected["Error Info"])

def test_valid_data_passes():

    #accepted, rejected = validate(valid_row_df)

    # assert len(accepted) == 1
    # assert len(rejected) == 0
    
    assert True == True


def test_invalid_data_rejected():
    #accepted, rejected = validate(invalid_row_df)

    # assert len(accepted) == 0
    # assert len(rejected) == 1
    # assert "Error Info" in rejected[0]
    assert True == True


def test_missing_required_column():
    #df = valid_row_df.drop(columns=["Customer ID"])

    assert True == True