from ..util.http_util import HttpUtil
from typing import Dict

class SystemSettings:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['system_settings']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers

    # file_paths need to be relative to the AnytingLLM installation with internal names 
    # ex: custom-documents/foo.txt-XXX.json
    def remove_documents(self, file_paths):
        files_to_remove = {
            "names": file_paths
        }
        remove_url = f"{self.base_url}/{self.endpoints['remove-documents']}"
        json_data = HttpUtil.safe_request(self.session, remove_url, self.headers, method='DELETE', data=files_to_remove)

        return json_data['success'] is True
    

    def update_env(self, settings: Dict[str, str]) -> bool:
        url = f"{self.base_url}/{self.endpoints['update-env']}"
        json_data = HttpUtil.safe_request(self.session, url, self.headers, method='POST', data=settings)

        return all(item in json_data['newValues'] for item in settings.keys())
        

    def update_setting(self, key: str, value: str) -> bool:
        return self.update_env({key: value})


    def get_env(self):
        url = f"{self.base_url}/{self.endpoints['get-env']}"
        json_data = HttpUtil.safe_request(self.session, url, self.headers, method='GET')

        return json_data['settings']

