import secrets
import string
from typing import List
from os.path import basename
from ..models.workspaces_model import Attachment, WorkspaceRequest, ChatRequest
from ..client import APIClient

class ChatSession:

    def __init__(self, mode: str, api_client: APIClient, workspace_slug: str = '', attachments: List[Attachment] = []):
        self.mode = mode
        self.session_id = self.generate_random_string()
        self.attachments = attachments
        self.api_client = api_client
        self._current_uploaded_docs = []   #keep track of currently uploaded files for final cleanup


        if workspace_slug == '':
            ws = WorkspaceRequest(name=self.generate_random_string(), chatMode=mode)
            workspace = self.api_client.workspaces.create_workspace(ws)
            self.workspace_slug = workspace.slug
        else:
            self.workspace_slug = workspace_slug

    
    @staticmethod
    def generate_random_string(length=16) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    

    def send(self, message: str) -> str:
        request = ChatRequest(message=message, mode=self.mode, sessionId=self.session_id, attachments=self.attachments)
        response = self.api_client.workspaces.chat_with_workspace(workspace_slug=self.workspace_slug, request=request)
        return response.textResponse

    
    def add_attachment(self, name: str, mime: str, content: str):
        self.attachments.append(Attachment(name=name, mime=mime, contentString=content))


    def remove_attachment(self, name: str):
        self.attachments = [attach for attach in self.attachments if attach.name != name]
    

    def embed(self, files_to_add: List[str] = [], files_to_remove: List[str] = []) -> bool:
        all_success, errors, docs_to_add = self.api_client.documents.upload_files(files_to_add)
        if not all_success:
            for error in errors:
                print(f'WARNING: file upload failed with error: {error}')

        self._current_uploaded_docs.extend(docs_to_add)

        docs_to_remove = [doc 
                          for doc in self._current_uploaded_docs 
                          for file in files_to_remove
                          if doc.title == basename(file)]
        remove_paths = [doc.location for doc in docs_to_remove]
        add_paths = [doc.location for doc in docs_to_add]

        is_success = self.api_client.workspaces.update_embeddings(
            self.workspace_slug, files_to_add=add_paths, files_to_remove=remove_paths)
        if not is_success:
            print("WARNING: embedding failed.")

        is_success = self.api_client.system_settings.remove_documents(remove_paths)
        if not is_success:
            print('WARNING: failed to remove files')
        self._current_uploaded_docs = [doc for doc in self._current_uploaded_docs if doc not in docs_to_remove]

        return is_success
    

    def cleanup(self, rm_workspace: bool, rm_uploaded_files: bool):
        if(rm_workspace):
            self.api_client.workspaces.delete_workspace(self.workspace_slug)

        if(rm_uploaded_files):
            remove_paths = [doc.location for doc in self._current_uploaded_docs]
            if len(remove_paths) != 0:
                self.api_client.system_settings.remove_documents(remove_paths)
                self._current_uploaded_docs.clear()
            