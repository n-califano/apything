def test_remove_documents(api_client, tmp_files):
    # Setup
    _, _, files = api_client.documents.upload_files(tmp_files)
    docs_to_remove = [file.location for file in files]

    json = api_client.system_settings.remove_documents(docs_to_remove)
    
    assert json['success'] is True
    assert json['message'] == "Documents removed successfully"