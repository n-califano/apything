import pytest
from apything import Workspace
import os.path
import json

# scope="session" --> runs only once for the entire test session, before running the tests
# scope="function" --> runs before every test
# autouse=True --> runs automatically without needing to be explicitly used in tests
@pytest.fixture
def test_workspace(api_client):
    # Setup
    ws_name = "test_workspace"
    ws = Workspace(ws_name, 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)
    yield ws_name
    # Teardown
    api_client.workspaces.delete_workspace(ws_name)


def test_update_embeddings(api_client, tmp_files, test_workspace):
    # Setup
    json_data = api_client.documents.upload_files(tmp_files)
    internal_files = [item['documents'][0]['location'] for item in json_data]
    
    # Embed file1 and file2
    json_data = api_client.workspaces.update_embeddings(test_workspace, internal_files[:-1])
    
    workspace = json_data['workspace']
    assert workspace['name'] == test_workspace
    assert workspace['slug'] == test_workspace
    docs = workspace['documents']
    assert len(docs) == 2
    for i, doc in enumerate(docs):
        assert doc['filename'].startswith(f"file{i+1}")
        assert doc['filename'].endswith(".json")
        assert doc['docpath'] == internal_files[i]
        assert doc['workspaceId'] == workspace['id']
        metadata = json.loads(doc['metadata'])
        assert metadata['id'] in internal_files[i]
        assert metadata['title'] == os.path.basename(tmp_files[i])

    # Remove file1 and file2, embed file3
    json_data = api_client.workspaces.update_embeddings(test_workspace, [internal_files[2]], internal_files[:-1])

    workspace = json_data['workspace']
    assert workspace['name'] == test_workspace
    assert workspace['slug'] == test_workspace
    docs = workspace['documents']
    assert len(docs) == 1
    doc = docs[0]
    assert doc['filename'].startswith("file3")
    assert doc['filename'].endswith(".json")
    assert doc['docpath'] == internal_files[2]
    assert doc['workspaceId'] == workspace['id']
    metadata = json.loads(doc['metadata'])
    assert metadata['id'] in internal_files[2]
    assert metadata['title'] == os.path.basename(tmp_files[2])

    # Teardown
    api_client.system_settings.remove_documents(internal_files)
    

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