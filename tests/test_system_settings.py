import pytest
import yaml
import os.path
from apything import APIClient

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
    
def test_remove_documents(api_client, tmp_files):
    # Setup
    json = api_client.documents.upload_files(tmp_files.values())
    docs_to_remove = [item['documents'][0]['location'] for item in json]

    json = api_client.system_settings.remove_documents(docs_to_remove)
    
    assert json['success'] is True
    assert json['message'] == "Documents removed successfully"