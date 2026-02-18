from src.data_cleaning import clean_data
import pandas as pd
import numpy as np

def test_string_titlecase():
    ### Test that cleaning properly capitalizes rows into title-case
    data = {"Transaction ID": ['TXN_6867343'],
            "Customer ID": ['CUST_12'],
            "Category": ['Patisserie'],
            "Item": ['Item_10_PAT'],      
            "Price Per Unit": [14.0],
            "Quantity": [2.0],        
            "Total Spent": [28.0],
            "Payment Method": ['Credit Card'], 
            "Location": ['in-store'],   # To be cleaned
            "Transaction Date": ['2022-10-05'],
            "Discount Applied": [True]}
    df = pd.DataFrame(data)
    
    df = clean_data(df)
    
    assert df.iloc[0]['Location'] == 'In-Store'

def test_string_id_format():
    ### Test that ids are properly formatted
    data = {"Transaction ID": ['TXN_6867343'],  # To be cleaned
            "Customer ID": ['CUST_12'],         # To be cleaned
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
    
    df = clean_data(df)

    assert df.iloc[0]['Transaction ID'] == 6867343
    assert df.iloc[0]['Customer ID'] == 12

def test_string_item_format():
    ### Test that items are properly formatted
    data = {"Transaction ID": ['TXN_6867343'],
            "Customer ID": ['CUST_12'],
            "Category": ['Patisserie'],
            "Item": ['Item_10_PAT'],    # To be cleaned     
            "Price Per Unit": [14.0],
            "Quantity": [2.0],        
            "Total Spent": [28.0],
            "Payment Method": ['Credit Card'], 
            "Location": ['In-Store'],   
            "Transaction Date": ['2022-10-05'],
            "Discount Applied": [True]}
    df = pd.DataFrame(data)
    
    df = clean_data(df)

    assert df.iloc[0]['Item'] == "10_PAT"

def test_numeric_conversion():
    ### Test that numerics are properly converted 
    data = {"Transaction ID": ['TXN_6867343'],
            "Customer ID": ['CUST_12'],
            "Category": ['Patisserie'],
            "Item": ['Item_10_PAT'],      
            "Price Per Unit": [14.0],
            "Quantity": ['2'],        
            "Total Spent": [28.0],
            "Payment Method": ['Credit Card'], 
            "Location": ['In-Store'],   
            "Transaction Date": ['2022-10-05'],
            "Discount Applied": [True]}
    df = pd.DataFrame(data)
    
    df = clean_data(df)

    assert isinstance(df.iloc[0]['Quantity'], (int, np.integer)) == True
    
def test_bool_conversion():
    ### Test that booleans are properly converted 
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
            "Discount Applied": ['yes']}    # To be cleaned
    df = pd.DataFrame(data)
    
    df = clean_data(df)

    assert isinstance(df.iloc[0]['Discount Applied'], np.bool_)

def test_date_format():
    ### Test that dates are properly formatted
    data = {"Transaction ID": ['TXN_6867343'],
            "Customer ID": ['CUST_12'],
            "Category": ['Patisserie'],
            "Item": ['Item_10_PAT'],      
            "Price Per Unit": [14.0],
            "Quantity": [2.0],        
            "Total Spent": [28.0],
            "Payment Method": ['Credit Card'], 
            "Location": ['In-Store'],   
            "Transaction Date": ['10-05-2022'], # To be cleaned
            "Discount Applied": [True]}
    df = pd.DataFrame(data)
    
    df = clean_data(df)

    assert "2022-10-05" in str(df.iloc[0]['Transaction Date'])