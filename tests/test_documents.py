import os.path


def test_upload_file(api_client, tmp_files):
    tmp_file = tmp_files[0]

    success, error, doc = api_client.documents.upload_file(tmp_file)
    
    assert success is True
    assert error is None
    assert doc.title == os.path.basename(tmp_file)
    assert doc.wordCount == 4
    assert doc.pageContent == tmp_file.read_text()
    assert doc.location.startswith('custom-documents')
    assert doc.location.endswith('json')
    assert doc.folder == 'custom-documents'
    assert doc.file_type == 'file'
    assert doc.cached is False
    assert doc.canWatch is False
    assert doc.watched is False
    assert doc.pinnedWorkspaces == []

    # Teardown
    api_client.system_settings.remove_documents([doc.location])


def test_upload_files(api_client, tmp_files):
    internal_files = []     #store internal docs paths for later removal

    success, errors, docs = api_client.documents.upload_files(tmp_files)
    assert len(docs) == 3
    assert success is True
    assert errors == []

    for i, tmp_file in enumerate(tmp_files):
        doc = docs[i]

        assert doc.title == os.path.basename(tmp_file)
        assert doc.wordCount == 4
        assert doc.pageContent == tmp_file.read_text()
        assert doc.location.startswith('custom-documents')
        assert doc.location.endswith('json')
        assert doc.folder == 'custom-documents'
        assert doc.file_type == 'file'
        assert doc.cached is False
        assert doc.canWatch is False
        assert doc.watched is False
        assert doc.pinnedWorkspaces == []

        internal_files.append(doc.location)
    
    # Teardown
    api_client.system_settings.remove_documents(internal_files)

def test_get_documents(api_client, tmp_files):
    # Setup
    _, _, files = api_client.documents.upload_files(tmp_files)
    internal_files = [file.location for file in files]

    docs = api_client.documents.get_documents()
    assert len(docs) == 3
    for i, doc in enumerate(docs):
        assert doc.folder == "custom-documents"
        assert doc.name.startswith(os.path.basename(tmp_files[i]))
        assert doc.file_type == "file"
        assert doc.id in internal_files[i]
        assert doc.title == os.path.basename(tmp_files[i])
        assert doc.wordCount == 4
        assert doc.cached is False
        assert doc.canWatch is False
        assert doc.watched is False
        assert doc.pinnedWorkspaces == []

    # Teardown
    api_client.system_settings.remove_documents(internal_files)
