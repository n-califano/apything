class Documents:
    def __init__(self, client):
        self.client = client  # Reference to APIClient
        self.endpoints = self.client.config['endpoints']['documents']
        self.session = self.client.session
        self.base_url = self.client.base_url
        self.headers = self.client.session.headers

    def upload_file(self, file_path):
        file_to_upload = {
            "file": open(file_path, "rb")
        }
        upload_url = f"{self.base_url}/{self.endpoints['upload']}"
        response = self.session.post(upload_url, headers=self.headers, files=file_to_upload)
        
        return response.json()
    
    def upload_files(self, file_paths):
        return [self.upload_file(file_path) for file_path in file_paths]
    
    def get_documents(self):
        docs_url = f"{self.base_url}/{self.endpoints['documents']}"
        response = self.session.get(docs_url, headers=self.headers)

        return response.json()