from dataclasses import dataclass, field
from typing import List, Literal, Optional
import json

# Note: decided to duplicate the attributes present in both request and response class. Inheritance caused
# trouble because non default argument need to be before default arguments otherwise you get:  
# TypeError: non-default argument 'id' follows default argument 
@dataclass
class WorkspaceRequest:
    name: str
    chatMode: str
    openAiTemp: float = 0.7
    openAiHistory: int = 20
    openAiPrompt: str = 'You are a helpful assistant.'
    similarityThreshold: float = 0.25
    topN: int = 4
    queryRefusalResponse: str = 'There is no relevant information in this workspace to answer your query.'


@dataclass
class WorkspaceResponse:
    id: int
    slug: str
    createdAt: str
    lastUpdatedAt: str
    vectorTag: str
    chatProvider: str
    chatModel: str
    pfpFilename: str
    agentProvider: str
    agentModel: str
    vectorSearchMode: str
    name: str
    chatMode: str
    openAiTemp: float = 0.7
    openAiHistory: int = 20
    openAiPrompt: str = 'You are a helpful assistant.'
    similarityThreshold: float = 0.25
    topN: int = 4
    queryRefusalResponse: str = 'There is no relevant information in this workspace to answer your query.'

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)
    

@dataclass
class WorkspaceDocument():
    id: int
    docId: str
    filename: str
    docpath: str
    workspaceId: int
    metadata: 'WorkspaceDocument.Metadata'
    pinned: bool
    watched: bool
    createdAt: str
    lastUpdatedAt: str

    @classmethod
    def from_json(cls, json_data: dict):
        metadata = json.loads(json_data.pop("metadata", {}))
        return cls(
            metadata=cls.Metadata.from_json(metadata),
            **json_data)
    
    @dataclass
    class Metadata:
        id: str
        url: str
        title: str
        docAuthor: str
        description: str
        docSource: str
        chunkSource: str
        published: str
        wordCount: int
        token_count_estimate: int

        @classmethod
        def from_json(cls, json_data: dict):
            return cls(**json_data)


@dataclass
class Workspace(WorkspaceResponse):
    documents: List[WorkspaceDocument] = field(default_factory=list)
    threads: List = field(default_factory=list)

    @classmethod
    def from_json(cls, json_data: dict):
        documents_data = json_data.pop("documents", [])
        threads_data = json_data.pop("threads", [])
        return cls(
            documents=[WorkspaceDocument.from_json(d) for d in documents_data],
            threads=threads_data,
            **json_data
        )
    

@dataclass
class Attachment():
    name: str
    mime: str
    contentString: str


@dataclass
class ChatRequest():
    message: str
    mode: Literal["query", "chat"]
    sessionId: str
    attachments: List[Attachment] = field(default_factory=list)


@dataclass
class ChatSource():
    title: str
    chunk: str


@dataclass
class ChatMetrics():
    prompt_tokens: int 
    completion_tokens: int 
    total_tokens: int 
    outputTps: float 
    duration: float


@dataclass
class ChatResponse():
    id: str
    type: Literal["abort", "textResponse"]
    textResponse: str
    sources: List[ChatSource]
    close: bool
    error: Optional[str]  # Can be None or a string describing the failure
    metrics: ChatMetrics
    chatId: int = None  # This property has a value only if using 'chat' mode, is None for 'query' mode

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)