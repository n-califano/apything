from ..models.documents_model import Document
from ..util.http_util import HttpUtil, ApythingRequestException

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
        json_data = HttpUtil.safe_request(self.session, upload_url, self.headers, method='POST', files=file_to_upload)
        doc = Document.from_json(json_data['documents'][0])

        return (json_data['success'] is True, json_data['error'], doc)
    
    def upload_files(self, file_paths):
        upload_responses = [self.upload_file(file_path) for file_path in file_paths]
        
        errors = []
        docs = []
        all_success = True
        for success, error, doc in upload_responses:
            docs.append(doc)
            if not success:
                all_success = False
                errors.append(error)

        return all_success, errors, docs
    
    def get_documents(self) -> list:
        docs_url = f"{self.base_url}/{self.endpoints['documents']}"
        json_data = HttpUtil.safe_request(self.session, docs_url, self.headers, method='GET')
        folders = json_data['localFiles']['items']
        docs = [Document.from_json(docItem, folder['name']) for folder in folders for docItem in folder['items']]
        
        return docs
    

    # WARNING: anythingLLM for this endpoint does not return information about the doc's folder, so 
    # doc.folder == "" in the doc object returned by this method
    def get_doc_by_name(self, doc_name: str) -> Document:
        endpoint = self.endpoints['document'].format(docName=doc_name)
        get_doc_url = f"{self.base_url}/{endpoint}"
        json_data = HttpUtil.safe_request(self.session, get_doc_url, self.headers, method='GET')
        
        return Document.from_json(json_data['document'])


    def create_folder(self, name: str) -> bool:
        new_folder = {
            'name' : name
        }

        url = f"{self.base_url}/{self.endpoints['create-folder']}"
        json_data = HttpUtil.safe_request(self.session, url, self.headers, method='POST', data=new_folder)

        if(not json_data['success']):
            raise ApythingRequestException(f"Error: {json_data['message']}")

        return json_data['success'] is True and json_data['message'] is None