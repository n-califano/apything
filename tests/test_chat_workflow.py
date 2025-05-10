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


def test_chat_session_image_attach(api_client):
    chat = ChatSession(mode='chat', api_client=api_client)

    with open("assets/equation.b64", 'r') as file:
        base64_uri = file.read()
        chat.add_attachment(name="equation.png", mime="image/png", content=base64_uri)

    response = chat.send("What is in the attached image?")

    chat.cleanup(True, True)

    assert "Mean Squared Error" or "MSE" in response


def test_add_and_remove_attachment(api_client):
    chat = ChatSession(mode='chat', api_client=api_client)

    chat.add_attachment(name="equation.png", mime="image/png", content='fake content')

    assert len(chat.attachments) == 1
    assert chat.attachments[0].name == 'equation.png'

    chat.remove_attachment(name='equation.png')

    assert len(chat.attachments) == 0
    