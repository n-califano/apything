import pytest
import yaml
import os.path
from apything import APIClient, Workspace

@pytest.fixture
def api_client():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.yml")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return APIClient(config['base_url'], config['api_key'])
    
@pytest.fixture
def tmp_files(tmp_path):
    files = [
        tmp_path / "file1.txt",
        tmp_path / "file2.txt",
        tmp_path / "file3.txt"
    ]
    for file_path in files:
        file_path.write_text(f"Fake content for {file_path}")
    return files

# scope="session" --> runs only once for the entire test session, before running the tests
# scope="function" --> runs before every test
# autouse=True --> runs automatically without needing to be explicitly used in tests
@pytest.fixture(scope="function", autouse=True)
def create_test_workspace(api_client):
    # Setup
    ws = Workspace("test_workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)
    yield
    # Teardown
    api_client.workspaces.delete_workspace("test_workspace")

#def test_update_embeddings(api_client, tmp_files):
    # Setup
    #api_client.documents.upload_files(tmp_files)
    
    #TODO: need to have a way to create a workspace before doing this!
    #json = api_client.workspaces.update_embeddings(tmp_files[:-1])
    #print(json)
    #assert False

def test_create_workspace(api_client):
    ws = Workspace("test create workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    json = api_client.workspaces.create_workspace(ws)
    workspace = json['workspace']

    assert workspace['name'] == "test create workspace"
    assert workspace['slug'] == "test-create-workspace"
    assert workspace['openAiTemp'] == 0.7
    assert workspace['openAiHistory'] == 20
    assert workspace['openAiPrompt'] == "Custom prompt"
    assert workspace['chatMode'] == "chat"
    assert workspace['queryRefusalResponse'] == "Custom refusal"
    assert workspace['topN'] == 4

    # Teardown
    api_client.workspaces.delete_workspace(workspace['slug'])

def test_delete_workspace(api_client):
    # Setup
    ws = Workspace("test delete workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)

    response = api_client.workspaces.delete_workspace("test-delete-workspace")
    assert response is True