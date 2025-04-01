from dataclasses import dataclass, asdict


@dataclass
class Workspace:
    name: str
    similarityThreshold: float
    openAiTemp: float
    openAiHistory: int
    openAiPrompt: str
    queryRefusalResponse: str
    chatMode: str
    topN: int


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

        print("****** DEBUG ******" )
        print(files_to_add)
        
        endpoint = self.endpoints['update-embeddings'].format(slug=workspace_slug)
        update_url = f"{self.base_url}/{endpoint}"
        response = self.session.post(update_url, headers=self.headers, json=files_to_embed)

        return response.json()
    

    def create_workspace(self, new_workspace: Workspace):
        json_payload = asdict(new_workspace)

        create_url = f"{self.base_url}/{self.endpoints['new']}"
        response = self.session.post(create_url, headers=self.headers, json=json_payload)

        return response.json()
    

    def delete_workspace(self, workspace_slug):
        endpoint = self.endpoints['delete'].format(slug=workspace_slug)
        delete_url = f"{self.base_url}/{endpoint}"
        response = self.session.delete(delete_url, headers=self.headers)

        return response.ok

