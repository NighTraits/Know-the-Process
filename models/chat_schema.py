from enum import StrEnum
from dataclasses import dataclass


class EROLE(StrEnum):
    USER = "User"
    ASSISTANT = "Assistant"


@dataclass
class IChat:
    role: EROLE
    message: str

class KEY(StrEnum):
    API_KEY = "API_KEY"
    GOOGLE_API_KEY = "GOOGLE_API_KEY"
    EMBEDDING = "EMBEDDING_MODEL"
    AGENT = "AGENT_MODEL"
    COLLECTION = "COLLECTION"
    
    CHAT_HISTORY = "CHAT_HISTORY"
    DATA = "DATA"