from dataclasses import dataclass
from os.path import basename, dirname

@dataclass
class Document:
    id: str 
    url: str 
    name: str
    title: str
    file_type: str 
    folder: str
    docAuthor: str 
    description: str
    docSource: str
    chunkSource: str 
    published: str
    wordCount: int
    pageContent: str 
    token_count_estimate: int
    location: str
    cached: bool
    canWatch: bool
    pinnedWorkspaces: list
    watched: bool


    @classmethod
    def from_json(cls, json_data: dict, folder: str=None):
        common_args = {
            k: json_data.get(k) for k in ('id', 'url', 'title',
                                           'docAuthor', 'description', 'docSource',
                                           'chunkSource', 'published', 'wordCount',
                                           'pageContent', 'token_count_estimate', 'location')
        }

        # Use unpacking for attributes that are present in all endpoints and
        # handle separately those attributes that are present only in a subset of the endpoints
        return cls(
            **common_args,
            name=json_data.get('name', basename(json_data.get('location', ""))),
            file_type=json_data.get('type', 'file'),
            folder=folder if folder else dirname(json_data.get('location', "")),
            cached=json_data.get('cached', False),
            canWatch=json_data.get('canWatch', False),
            pinnedWorkspaces=json_data.get('pinnedWorkspaces', []),
            watched=json_data.get('watched', False))