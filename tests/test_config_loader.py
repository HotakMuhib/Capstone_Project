from src.config_loader import load_yaml

def test_load_yaml(tmp_path):
    file = tmp_path / "test.yaml"
    file.write_text("key: value")

    result = load_yaml(str(file))

    assert result["key"] == "value"