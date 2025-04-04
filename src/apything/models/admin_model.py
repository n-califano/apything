from dataclasses import dataclass

@dataclass
class User:
    id: int 
    username: str
    pfpFilename: str 
    role: str
    suspended: int
    seen_recovery_codes: bool 
    createdAt: str
    lastUpdatedAt: str
    dailyMessageLimit: int

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)