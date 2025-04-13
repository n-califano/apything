import os.path
import pytest
from apything import ApythingRequestException


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


def test_get_doc_by_name_success(api_client, tmp_uploaded_files):
    for file in tmp_uploaded_files:
        doc = api_client.documents.get_doc_by_name(file.name)

        assert doc.name == file.name
        assert doc.file_type == 'file'
        assert doc.id == file.id
        assert doc.url == file.url
        assert doc.title == file.title
        assert doc.docAuthor == file.docAuthor
        assert doc.description == file.description


def test_get_doc_by_name_non_existent_doc_name_failure(api_client):
    with pytest.raises(ApythingRequestException) as ex:
        api_client.documents.get_doc_by_name("non existent doc name")

    expected_exception_msg = 'Error 404: Not Found'
    assert expected_exception_msg in str(ex.value)    


#def test_create_folder_success(api_client):
    #is_success = api_client.documents.create_folder("new folder")

    #assert is_success is True

    # Teardown
    # TODO: Currently there is no endpoint to remove a folder so teardown is not possible.
    # To avoid leaving test data leftovers in the anythingLLM instance, we postpone the implementation
    # of this test to when such endpoint will be available


#def test_create_folder_already_exist_failure(api_client):
    # TODO: Currently there is no endpoint to remove a folder so teardown is not possible.
    # To avoid leaving test data leftovers in the anythingLLM instance, we postpone the implementation
    # of this test to when such endpoint will be available