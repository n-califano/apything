import pytest
import yaml
import os.path
from apything import APIClient, WorkspaceRequest

# These fixtures can be used by all tests, avoiding the copy-paste of identical fixtures. 
# Fixtures are re-created for each test that uses them.

@pytest.fixture
def api_client():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.yml")
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return APIClient(config['base_url'], config['api_key'])


@pytest.fixture
def tmp_files(tmp_path):
    files = [
        tmp_path / "file1.txt",
        tmp_path / "file2.txt",
        tmp_path / "file3.txt"
    ]
    for file_path in files:
        file_path.write_text(f"Fake content for {file_path}")
    return files


# scope="session" --> runs only once for the entire test session, before running the tests
# scope="function" --> runs before every test
# autouse=True --> runs automatically without needing to be explicitly used in tests
@pytest.fixture
def test_workspace(api_client):
    # Setup
    ws = WorkspaceRequest("test_workspace", 0.7, 0.7, 20, "Custom prompt", "Custom refusal", "chat", 4)
    ws_response = api_client.workspaces.create_workspace(ws)
    yield ws_response
    # Teardown
    api_client.workspaces.delete_workspace(workspace_slug=ws_response.slug)