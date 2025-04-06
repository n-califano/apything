import pytest
from apything import WorkspaceRequest

# scope="session" --> runs only once for the entire test session, before running the tests
# scope="function" --> runs before every test
# autouse=True --> runs automatically without needing to be explicitly used in tests
@pytest.fixture
def test_workspace(api_client):
    # Setup
    ws_name = "test_workspace"
    ws = WorkspaceRequest(ws_name, 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)
    yield ws_name
    # Teardown
    api_client.workspaces.delete_workspace(ws_name)


def test_update_embeddings(api_client, tmp_files, test_workspace):
    # Setup
    _, _, files = api_client.documents.upload_files(tmp_files)
    internal_files = [file.location for file in files]
    
    # Embed file1 and file2
    is_success = api_client.workspaces.update_embeddings(test_workspace, internal_files[:-1])
    assert is_success is True
    
    # Remove file1 and file2, embed file3
    is_success = api_client.workspaces.update_embeddings(test_workspace, [internal_files[2]], internal_files[:-1])
    assert is_success is True

    # Teardown
    api_client.system_settings.remove_documents(internal_files)
    

def test_create_workspace(api_client):
    ws = WorkspaceRequest(name="test create workspace", similarityThreshold=0.7, openAiTemp=0.7, 
                        openAiHistory=20, openAiPrompt="Custom prompt", queryRefusalResponse="Custom refusal", 
                        chatMode="chat", topN=4)
    workspace = api_client.workspaces.create_workspace(ws)

    assert workspace.name == "test create workspace"
    assert workspace.slug == "test-create-workspace"
    assert workspace.openAiTemp == 0.7
    assert workspace.openAiHistory == 20
    assert workspace.openAiPrompt == "Custom prompt"
    assert workspace.chatMode == "chat"
    assert workspace.queryRefusalResponse == "Custom refusal"
    assert workspace.topN == 4

    # Teardown
    api_client.workspaces.delete_workspace(workspace.slug)


def test_delete_workspace(api_client):
    # Setup
    ws = WorkspaceRequest("test delete workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)

    is_success = api_client.workspaces.delete_workspace("test-delete-workspace")
    assert is_success is True