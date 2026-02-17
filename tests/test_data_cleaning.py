from data_cleaning import clean_data

def test_string_formatting(valid_row_df):
    df = clean_data(valid_row_df)

    assert df["Payment Method"].iloc[0] == "Credit Card"
    assert df["Location"].iloc[0] == "Online"
    assert df["Category"].iloc[0] == "Electronics"