def test_remove_documents(api_client, tmp_files):
    # Setup
    json = api_client.documents.upload_files(tmp_files.values())
    docs_to_remove = [item['documents'][0]['location'] for item in json]

    json = api_client.system_settings.remove_documents(docs_to_remove)
    
    assert json['success'] is True
    assert json['message'] == "Documents removed successfully"