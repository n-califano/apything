class Document:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.url = f"{self.client.base_url}/document"

    def upload_file(self, file_path):
        file_to_upload = {
            "file": open(file_path, "rb")
        }
        upload_url = f"{self.url}/upload"
        response = self.client.session.post(upload_url, headers=self.client.session.headers, files=file_to_upload)
        
        return response.json()
    
    def upload_files(self, file_paths):
        return [self.upload_file(file_path) for file_path in file_paths]