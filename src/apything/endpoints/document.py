class Document:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['documents']

    def upload_file(self, file_path):
        file_to_upload = {
            "file": open(file_path, "rb")
        }
        upload_url = f"{self.client.base_url}/{self.endpoints['upload']}"
        response = self.client.session.post(upload_url, headers=self.client.session.headers, files=file_to_upload)
        
        return response.json()
    
    def upload_files(self, file_paths):
        return [self.upload_file(file_path) for file_path in file_paths]