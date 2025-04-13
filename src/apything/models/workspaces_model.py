from dataclasses import dataclass, field
from typing import List, Literal, Optional


@dataclass
class WorkspaceRequest:
    name: str
    openAiTemp: float 
    openAiHistory: int 
    openAiPrompt: str
    similarityThreshold: float 
    topN: int
    chatMode: str
    queryRefusalResponse: str


@dataclass
class WorkspaceResponse(WorkspaceRequest):
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

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)
    

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