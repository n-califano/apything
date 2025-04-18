import pytest
import string
import secrets
from apything import WorkspaceRequest, ChatRequest, WorkspaceResponse, Attachment, ApythingRequestException


@pytest.fixture
def random_session_id(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def test_update_embeddings(api_client, tmp_files, test_workspace):
    # Setup
    _, _, files = api_client.documents.upload_files(tmp_files)
    internal_files = [file.location for file in files]
    
    # Embed file1 and file2
    is_success = api_client.workspaces.update_embeddings(test_workspace.slug, internal_files[:-1])
    assert is_success is True
    
    # Remove file1 and file2, embed file3
    is_success = api_client.workspaces.update_embeddings(test_workspace.slug, [internal_files[2]], internal_files[:-1])
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


def test_create_workspace_only_name_and_mode(api_client):
    ws = WorkspaceRequest(name="test create workspace", chatMode="query")
    workspace = api_client.workspaces.create_workspace(ws)

    assert workspace.name == "test create workspace"
    assert workspace.slug == "test-create-workspace"
    assert workspace.chatMode == "query"

    # Teardown
    api_client.workspaces.delete_workspace(workspace.slug)


def test_delete_workspace(api_client):
    # Setup
    ws = WorkspaceRequest("test delete workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    api_client.workspaces.create_workspace(ws)

    is_success = api_client.workspaces.delete_workspace("test-delete-workspace")
    assert is_success is True


def test_chat_with_workspace_no_attachments_success(api_client, random_session_id: str, test_workspace: WorkspaceResponse):
    request = ChatRequest(message="My hair is blue", mode="chat", sessionId=random_session_id)
    response = api_client.workspaces.chat_with_workspace(workspace_slug=test_workspace.slug, request=request)

    assert response.id is not None and response.id != ""
    assert response.type == "textResponse"
    assert response.textResponse is not None and response.textResponse != ""
    assert response.error is None

    request = ChatRequest(message="Do you remember what colors my hair is?", mode="chat", sessionId=random_session_id)
    response = api_client.workspaces.chat_with_workspace(workspace_slug=test_workspace.slug, request=request)

    assert response.id is not None and response.id != ""
    assert response.type == "textResponse"
    # Here we check that the session actually persisted (same sessionId) and the model is able to give us 
    # information based on our previous request
    assert "blue" in response.textResponse.lower()
    assert response.error is None


# WARNING: depending on the LLM used you could get an error. I tested it with the Gemini API and to make it work
# I had to set the Safety Setting in the LLM Preferences to 'None'. With the default setting ('Block some') i kept
# getting a 'Candidate was blocked due to SAFETY' error.
def test_chat_with_workspace_with_attachments_success(api_client, random_session_id: str, test_workspace: WorkspaceResponse):
    with open("assets/art.b64", 'r') as file:
        base64_uri = file.read()
    
    attachment = Attachment(name="art.webp", mime="image/webp", contentString=base64_uri)
    request = ChatRequest(message="What's in the attached file?", mode="chat", sessionId=random_session_id, attachments=[attachment])
    response = api_client.workspaces.chat_with_workspace(workspace_slug=test_workspace.slug, request=request)
    text = response.textResponse.lower()
        
    assert response.id is not None and response.id != ""
    assert response.type == "textResponse"
    assert "art" in text or "clown" in text
    assert response.error is None


def test_chat_with_workspace_query_mode_success(api_client, random_session_id: str, test_workspace):
    # Setup
    _, _, doc = api_client.documents.upload_file(file_path="assets/nytheris.txt")
    is_success = api_client.workspaces.update_embeddings(test_workspace.slug, [doc.location])
    if not is_success:
        raise Exception("The embedding of the file failed.")
    
    request = ChatRequest(message="What are the rumors about Nytheris Prime?", mode="query", sessionId=random_session_id)
    response = api_client.workspaces.chat_with_workspace(workspace_slug=test_workspace.slug, request=request)
    text = response.textResponse.lower()

    assert response.id is not None and response.id != ""
    assert response.type == "textResponse"
    assert "sentient weather systems" in text and "time fractures" in text
    assert response.error is None
    
    # Teardown
    api_client.system_settings.remove_documents([doc.location])


def test_chat_with_workspace_unsupported_mode_failure(api_client, random_session_id: str, test_workspace):
    request = ChatRequest(message="Hello there", mode="unsupported-mode", sessionId=random_session_id)
    
    with pytest.raises(ApythingRequestException) as ex:
        api_client.workspaces.chat_with_workspace(workspace_slug=test_workspace.slug, request=request)

    expected_exception_msg = 'Error 400: unsupported-mode is not a valid mode.'
    assert expected_exception_msg in str(ex.value)


def test_get_workspace(api_client, test_workspace, tmp_embedded_files):
    ws = api_client.workspaces.get_workspace(test_workspace.slug)

    assert ws.slug == 'test_workspace'
    assert ws.name == 'test_workspace'
    assert ws.chatMode == 'chat'
    assert len(ws.documents) == 3
    for i, doc in enumerate(ws.documents):
        assert doc.metadata.title == tmp_embedded_files[i].title
        assert doc.filename == tmp_embedded_files[i].name
        assert doc.docpath == tmp_embedded_files[i].location
        assert doc.metadata.id == tmp_embedded_files[i].id
        assert doc.metadata.url == tmp_embedded_files[i].url
        assert doc.metadata.wordCount == tmp_embedded_files[i].wordCount
        assert doc.metadata.token_count_estimate == tmp_embedded_files[i].token_count_estimate