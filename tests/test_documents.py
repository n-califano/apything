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


def test_upload_file(api_client, tmp_files):
    tmp_file = tmp_files['file1']

    json = api_client.documents.upload_file(tmp_file)
    
    assert json['success'] is True
    assert json['error'] is None
    assert len(json['documents']) == 1
    document = json['documents'][0]
    assert document['title'] == os.path.basename(tmp_file)
    assert document['wordCount'] == 4
    assert document['pageContent'] == tmp_file.read_text()
    assert document['location'].startswith('custom-documents')
    assert document['location'].endswith('json')

    # Teardown
    api_client.system_settings.remove_documents([document['location']])


def test_upload_files(api_client, tmp_files):
    internal_files = []     #store internal docs paths for later removal

    json = api_client.documents.upload_files(tmp_files.values())
    assert len(json) == 3
    
    for i, tmp_file in enumerate(tmp_files.values()):
        item = json[i]
        document = item['documents'][0]

        assert item['success'] is True
        assert item['error'] is None
        assert len(item['documents']) == 1
        assert document['title'] == os.path.basename(tmp_file)
        assert document['wordCount'] == 4
        assert document['pageContent'] == tmp_file.read_text()
        assert document['location'].startswith('custom-documents')
        assert document['location'].endswith('json')

        internal_files.append(document['location'])
    
    # Teardown
    api_client.system_settings.remove_documents(internal_files)

def test_get_documents(api_client, tmp_files):
    # Setup
    tmp_files = list(tmp_files.values())
    json = api_client.documents.upload_files(tmp_files)
    internal_files = [item['documents'][0]['location'] for item in json]

    json = api_client.documents.get_documents()
    folder = json['localFiles']['items'][0]
    assert folder['name'] == "custom-documents"
    assert folder['type'] == "folder"
    files = folder['items']
    assert len(files) == 3
    for i, file in enumerate(files):
        assert file['name'].startswith(os.path.basename(tmp_files[i]))
        assert file['type'] == "file"
        assert file['id'] in internal_files[i]
        assert file['title'] == os.path.basename(tmp_files[i])
        assert file['wordCount'] == 4

    # Teardown
    api_client.system_settings.remove_documents(internal_files)