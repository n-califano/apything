from os.path import basename
from apything import ChatSession

def test_chat_session_success(api_client):
    chat = ChatSession(mode='chat', api_client=api_client)
    response = chat.send("I like trains.")

    assert response != ''

    response = chat.send('What do i like?')

    assert 'trains' in response.lower()

    # Teardown
    chat.cleanup(True, True)


def test_chat_session_embed(api_client, tmp_files):
    chat = ChatSession(mode='chat', api_client=api_client)
    chat.embed(files_to_add=tmp_files[:-1])

    workspace = api_client.workspaces.get_workspace(chat.workspace_slug)
    embed_file_names = [doc.metadata.title for doc in workspace.documents]
    
    assert basename(tmp_files[0]) in embed_file_names
    assert basename(tmp_files[1]) in embed_file_names
    assert basename(tmp_files[2]) not in embed_file_names

    chat.embed(files_to_remove=tmp_files[:-1], files_to_add=[tmp_files[-1]])
    
    workspace = api_client.workspaces.get_workspace(chat.workspace_slug)
    embed_file_names = [doc.metadata.title for doc in workspace.documents]
    docs = api_client.documents.get_documents()
    doc_file_names = [doc.title for doc in docs] 

    assert basename(tmp_files[0]) not in embed_file_names
    assert basename(tmp_files[1]) not in embed_file_names
    assert basename(tmp_files[2]) in embed_file_names
    assert len(doc_file_names) == 1
    assert basename(tmp_files[0]) not in doc_file_names
    assert basename(tmp_files[1]) not in doc_file_names
    assert basename(tmp_files[2]) in doc_file_names

    chat.cleanup(rm_workspace=True, rm_uploaded_files=True)

    docs = api_client.documents.get_documents()
    workspace = api_client.workspaces.get_workspace(chat.workspace_slug)

    assert len(docs) == 0
    assert workspace is None
