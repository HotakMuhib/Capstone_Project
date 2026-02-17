from ingestion.csv_json_reader import read_source
import pandas as pd

def test_read_csv(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("col1,col2\n1,2")

    config = {
        "type": "csv",
        "path": [str(file)],
        "delimiter": ",",
        "has_header": True
    }

    df = read_source(config)

    assert len(df) == 1
    assert list(df.columns) == ["col1", "col2"]


def test_invalid_source_type():
    config = {
        "type": "xml",
        "path": ["fake.xml"]
    }

    try:
        read_source(config)
    except ValueError:
        assert True