from dataclasses import dataclass


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
