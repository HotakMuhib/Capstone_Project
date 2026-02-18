from src.deduplication import deduplicate
import pandas as pd

def test_deduplicate_transaction_id():
    ### Test that deduplicate rejects a second row with an already existing transaction id
    data = {"Transaction ID": [6867343, 6867343],
            "Customer ID": [12, 3],
            "Category": ['Patisserie', 'Electric Household Essentials'],
            "Item": ['10_PAT', '13_EHE'],      
            "Price Per Unit": [14.0, 23.0],
            "Quantity": [2, 1],        
            "Total Spent": [28.0, 23.0],
            "Payment Method": ['Credit Card', 'Digital Wallet'], 
            "Location": ['In-Store', 'Online'],   
            "Transaction Date": ['2022-10-05', '2022-02-07'],
            "Discount Applied": [True, False]}
    df = pd.DataFrame(data)

    accepted, rejected = deduplicate(df)

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]['Error Info'] == "Duplicate primary key"

def test_deduplicate_unique_identifiers():
    ### Tests that deduplication rejects a second row that has an existing subset of values in the unique identifiers
    data = {"Transaction ID": [6867343, 6867344],
            "Customer ID": [12, 12],
            "Category": ['Patisserie', 'Patisserie'],
            "Item": ['10_PAT', '10_PAT'],      
            "Price Per Unit": [14.0, 14.0],
            "Quantity": [2, 2],        
            "Total Spent": [28.0, 28.0],
            "Payment Method": ['Credit Card', 'Credit Card'], 
            "Location": ['In-Store', 'In-Store'],   
            "Transaction Date": ['2022-10-05', '2022-10-05'],
            "Discount Applied": [True, False]}
    df = pd.DataFrame(data)

    accepted, rejected = deduplicate(df)

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]['Error Info'] == "Duplicate subset of unique identifiers"