from ..models.admin_model import User
from ..util.http_util import HttpUtil

class Admin:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['admin']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers

    def get_users(self):
        users_url = f"{self.base_url}/{self.endpoints['users']}"
        json_data = HttpUtil.safe_request(self.session, users_url, self.headers, method='GET')

        return [User.from_json(json_item) for json_item in json_data['users']]