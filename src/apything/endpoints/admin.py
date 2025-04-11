from ..models.admin_model import User
from ..util.http_util import HttpUtil, ApythingRequestException


class Admin:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['admin']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers


    def get_users(self) -> list:
        users_url = f"{self.base_url}/{self.endpoints['users']}"
        json_data = HttpUtil.safe_request(self.session, users_url, self.headers, method='GET')

        return [User.from_json(json_item) for json_item in json_data['users']]
    

    def create_user(self, username: str, password: str, role: str) -> int:
        user_to_add = {
            "username": username,
            "password": password,
            "role": role
        }

        create_url = f"{self.base_url}/{self.endpoints['new']}"
        json_data = HttpUtil.safe_request(self.session, create_url, self.headers, method='POST', data=user_to_add)

        return json_data['user']['id']
    

    def remove_user(self, user_id: int) -> bool:
        endpoint = self.endpoints['delete'].format(id=user_id)
        delete_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, delete_url, self.headers, method='DELETE')

        if(not json_data['success']):
            raise ApythingRequestException(f"Error: {json_data['error']}")

        return json_data['success'] is True and json_data['error'] is None
    

    def assign_workspace_to_users(self, workspace_slug: int, user_ids: list, reset: bool = False) -> bool:
        users = {
            "userIds": user_ids,
            "reset": reset
        }

        endpoint = self.endpoints['manage-users'].format(workspaceSlug=workspace_slug)
        assign_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, assign_url, self.headers, method='POST', data=users)

        if(not json_data['success']):
            raise ApythingRequestException(f"Error: {json_data['error']}")

        return json_data['success'] is True and json_data['error'] is None
    

    def get_allowed_users_for_workspace(self, workspace_id: str) -> list:
        endpoint = self.endpoints['ws-users'].format(workspaceId=workspace_id)
        ws_users_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, ws_users_url, self.headers, method='GET')

        return [(user['userId'], user['role']) for user in json_data['users']]
    

    def update_user(self, user_id: int, new_username: str=None, new_password: str=None, new_role: str=None, is_suspended: bool=None) -> bool:
        updated_values = {
            key: value for key, value in {
                "username": new_username,
                "password": new_password,
                "role": new_role,
                "suspended": 1 if is_suspended else 0
            }.items() if value is not None
        }

        endpoint = self.endpoints['update'].format(id=user_id)
        update_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, update_url, self.headers, method='POST', data=updated_values)

        if(not json_data['success']):
            raise ApythingRequestException(f"Error: {json_data['error']}")

        return json_data['success'] is True and json_data['error'] is None