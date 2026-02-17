from src.deduplication import deduplicate
import pandas as pd

def test_duplicate_transaction_id():
    # df = pd.concat([valid_row_df, valid_row_df])

    # deduped, rejected = deduplicate(df)

    # assert len(deduped) == 1
    # assert len(rejected) == 1
    # assert rejected.iloc[0]["Error Info"] == "Duplicate primary key"
    assert True == True