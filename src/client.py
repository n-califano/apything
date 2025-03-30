import requests
import yaml
from endpoints.document import Document

class APIClient:
    def __init__(self, base_url, api_key, version='v1'):
        with open("../config/config.yml", "r") as config_file:
            self.config = yaml.safe_load(config_file)

        self.api_key = api_key
        self.base_url = f"{base_url}{self.config[version]}"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

        # Initialize submodules
        self.document = Document(self)



