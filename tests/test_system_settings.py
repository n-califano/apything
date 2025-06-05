def test_remove_documents(api_client, tmp_files):
    # Setup
    _, _, files = api_client.documents.upload_files(tmp_files)
    docs_to_remove = [file.location for file in files]

    is_success = api_client.system_settings.remove_documents(docs_to_remove)
    
    assert is_success is True

def test_update_env(api_client):
    current_settings = api_client.system_settings.get_env()
    disable_telemetry: bool = current_settings['DisableTelemetry'] == "True"

    settings = {
        "DisableTelemetry" : "False" if disable_telemetry else "True",
    }
    is_success = api_client.system_settings.update_env(settings)

    current_settings = api_client.system_settings.get_env()

    assert is_success
    assert (current_settings['DisableTelemetry'] == ("False" if disable_telemetry else "True"))

    # Teardown
    settings = {
        "DisableTelemetry" : "True" if disable_telemetry else "False",
    }
    # Restore previous situation
    api_client.system_settings.update_env(settings)


def test_add_setting_item(api_client):
    # Setup
    current_settings = api_client.system_settings.get_env()
    disable_telemetry: bool = current_settings['DisableTelemetry'] == "True"

    is_success = api_client.system_settings.add_setting_item(
        "DisableTelemetry", 
        "False" if disable_telemetry else "True")

    current_settings = api_client.system_settings.get_env()

    assert is_success
    assert (current_settings['DisableTelemetry'] == ("False" if disable_telemetry else "True"))

    # Teardown
    settings = {
        "DisableTelemetry" : "True" if disable_telemetry else "False",
    }
    # Restore previous situation
    api_client.system_settings.update_env(settings)


def test_get_env(api_client):
    current_settings = api_client.system_settings.get_env()

    assert len(current_settings) > 0