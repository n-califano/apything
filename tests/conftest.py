import pytest
import yaml
import os.path
from apything import APIClient

# These fixtures can be used by all tests, avoiding the copy-paste of identical fixtures. 
# Fixtures are re-created for each test that uses them.

@pytest.fixture
def api_client():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.yml")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return APIClient(config['base_url'], config['api_key'])

@pytest.fixture
def tmp_files(tmp_path):
    files = {
        "file1": tmp_path / "file1.txt",
        "file2": tmp_path / "file2.txt",
        "file3": tmp_path / "file3.txt"
    }
    for file_name, file_path in files.items():
        file_path.write_text(f"Fake content for {file_name}")
    return files