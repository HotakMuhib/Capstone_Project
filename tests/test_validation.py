from validation import validate
import pytest

def test_valid_data_passes(valid_row_df):
    accepted, rejected = validate(valid_row_df)

    assert len(accepted) == 1
    assert len(rejected) == 0


def test_invalid_data_rejected(invalid_row_df):
    accepted, rejected = validate(invalid_row_df)

    assert len(accepted) == 0
    assert len(rejected) == 1
    assert "Error Info" in rejected[0]


def test_missing_required_column(valid_row_df):
    df = valid_row_df.drop(columns=["Customer ID"])

    with pytest.raises(Exception):
        validate(df)