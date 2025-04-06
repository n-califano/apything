from dataclasses import asdict
from ..util.http_util import HttpUtil
from ..models.workspaces_model import WorkspaceResponse, WorkspaceRequest


class Workspaces:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['workspaces']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers


    def update_embeddings(self, workspace_slug, files_to_add = [], files_to_remove = []):
        files_to_embed = {
            "adds": files_to_add,
            "deletes": files_to_remove
        }
        
        endpoint = self.endpoints['update-embeddings'].format(slug=workspace_slug)
        update_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, update_url, self.headers, method='POST', data=files_to_embed)

        return json_data['workspace'] is not None
    

    def create_workspace(self, new_workspace: WorkspaceRequest):
        json_payload = asdict(new_workspace)
        create_url = f"{self.base_url}/{self.endpoints['new']}"
        json_data = HttpUtil.safe_request(self.session, create_url, self.headers, method='POST', data=json_payload)

        return WorkspaceResponse.from_json(json_data['workspace'])
    

    def delete_workspace(self, workspace_slug):
        endpoint = self.endpoints['delete'].format(slug=workspace_slug)
        delete_url = f"{self.base_url}/{endpoint}"
        is_success = HttpUtil.safe_request(self.session, delete_url, self.headers, method='DELETE')

        return is_success

