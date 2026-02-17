# tests/ directory will contain all tests
# may need to create several new test files here to test each file in src/

import pytest
import pandas as pd

@pytest.fixture
def valid_row_df():
    return pd.DataFrame({
        "Transaction ID": ["1001"],
        "Customer ID": ["2001"],
        "Category": ["electronics"],
        "Item": ["123_tv"],
        "Price Per Unit": [100.0],
        "Quantity": [2],
        "Total Spent": [200.0],
        "Payment Method": ["credit card"],
        "Location": ["online"],
        "Transaction Date": ["2024-01-01"],
        "Discount Applied": [False]
    })


@pytest.fixture
def invalid_row_df():
    return pd.DataFrame({
        "Transaction ID": ["abc"],  # invalid format
        "Customer ID": [None],      # missing
        "Category": ["electronics"],
        "Item": ["wrongformat"],
        "Price Per Unit": [-5],
        "Quantity": [0],
        "Total Spent": [-10],
        "Payment Method": ["bitcoin"],
        "Location": ["moon"],
        "Transaction Date": ["invalid-date"],
        "Discount Applied": [False]
    })